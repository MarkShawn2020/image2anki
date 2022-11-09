"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 09, 2022, 12:57
"""
from typing import List

import numpy as np
from PIL import ImageFilter, Image, ImageDraw

from src.parseLZY.ds import Block, HeadType, BaseBlock, FONT, HeadTypeColorMap
from src.parseLZY.settings import MIN_BLOCK_IS_PROBLEM_PCT, MIN_BLOCK_HEIGHT, MIN_HEIGHT_BETWEEN_BLOCKS, \
    MIN_NON_WHITE_POINTS_IN_ROW, MARGIN_LEFT_PCT, TOP_PCT, BOTTOM_PCT, DRAW_BLOCK_TYPE_SQUARE_SIZE, MERGE_CONTOURS, \
    DRAW_BLUE_XS, DRAW_BLOCK_TYPE, DRAW_BLOCK_CONTOUR, DRAW_BLOCK_COORDS, DRAW_HEIGHT_BETWEEN_BLOCKS, QR_RADIUS, \
    QR_PADDING_LEFT, QR_HALF_SIZE, QR_BLUR_MIN, MIN_BLUE_X, MAX_BLUE_X


def is_point_blue(p):
    """
    原先用的 2 * B / (R + G) 结果有些页面跑不通过
    B / R 也不可以
    要用 B / G，也就是蓝色显著比绿色多
    :param p:
    :return:
    """
    ans = p[2] / (p[1] + 1e-10) > 1
    #     print({"p": p, "ans": ans})
    return ans


def mergeBlocks(blocks: List[Block]) -> List[Block]:
    out = []
    start = end = None
    isCollecting = False
    for cur in blocks:
        cType = cur['headType']
        if cType == HeadType.PROBLEM:
            if isCollecting:
                out.append({"value": (start, end)})
            start, end = cur['value']
            isCollecting = True
        if cType == HeadType.TITLE:
            if isCollecting:
                out.append({"value": (start, end)})
                isCollecting = False
        if cType == HeadType.CONTINUE:
            if not start:
                start, end = cur['value']
                isCollecting = True
            if isCollecting:
                end = cur['value'][1]
    if isCollecting:
        out.append({"value": (start, end)})
    return out


def dropQrCode(img):
    w, h = img.size
    while True:
        im_blur = img.convert('L').filter(ImageFilter.BoxBlur(QR_RADIUS))
        blur_min = np.min(im_blur)
        if blur_min < QR_BLUR_MIN:
            qr_center = np.unravel_index(np.argmin(im_blur), (h, w))
            y, x = qr_center
            print(f'dropping qrcode at ({x}, {y}), val: {blur_min}')
            qr_start = (x - QR_HALF_SIZE - QR_PADDING_LEFT, y - QR_HALF_SIZE)
            img_white = Image.new(
                'RGB', (QR_HALF_SIZE * 2 + QR_PADDING_LEFT, QR_HALF_SIZE << 1), color=(255, 255, 255))
            img.paste(img_white, qr_start)
        else:
            break


def getBaseBlocks(img) -> List[BaseBlock]:
    w, h = img.size
    # 0: white, 1: others
    data = 1 - np.array(img.convert('1'))
    rows = np.apply_along_axis(lambda row: row.sum(axis=0), 1, data)
    assert rows.shape[0] == h, '对每一行进行二值化累计，因此高度保持不变'
    # print(rows.shape)

    blocks: List[BaseBlock] = []
    start = 0
    is_white = True
    for i, j in enumerate(rows):
        if i < TOP_PCT * h or i > BOTTOM_PCT * h:
            continue
        # 空白结束，内容开始
        if j >= MIN_NON_WHITE_POINTS_IN_ROW and is_white:
            start = i
            is_white = False
        # 内容结束，空白开始
        elif j < MIN_NON_WHITE_POINTS_IN_ROW and not is_white:
            is_white = True
            if i - start >= MIN_BLOCK_HEIGHT:
                if blocks and start - blocks[-1]['value'][1] < MIN_HEIGHT_BETWEEN_BLOCKS:
                    blocks[-1]['value'] = (blocks[-1]['value'][0], i)
                else:
                    blocks.append({"value": (start, i)})
    return blocks


def doDraw(img, base_blocks: List[BaseBlock]):
    w, h = img.size
    draw = ImageDraw.Draw(img)

    if MERGE_CONTOURS:
        blocks = mergeBlocks(base_blocks)

    if DRAW_BLUE_XS:
        draw.rectangle((MIN_BLUE_X, int(.01 * h), MAX_BLUE_X, int((TOP_PCT - .01) * h)), fill='blue')

    for block in base_blocks:
        y0, y1 = block['value']

        if DRAW_BLOCK_COORDS:
            draw.text(
                (0, y0),
                f'{y0}',
                font=FONT,
                fill='magenta',
                stroke_width=1
            )
            draw.text(
                (0, y1 - 50),
                f'{y1}',
                font=FONT,
                fill='magenta',
                stroke_width=1
            )

        if DRAW_BLOCK_CONTOUR:
            draw.rectangle(
                (MARGIN_LEFT_PCT * w, y0, w - MARGIN_LEFT_PCT * w * 2, y1),
                outline='red'
            )

        if DRAW_BLOCK_TYPE and not MERGE_CONTOURS:
            draw.rectangle(
                (MARGIN_LEFT_PCT * w, y0, MARGIN_LEFT_PCT * w +
                 DRAW_BLOCK_TYPE_SQUARE_SIZE, y0 + DRAW_BLOCK_TYPE_SQUARE_SIZE),
                fill=HeadTypeColorMap[block['headType']]
            )

    for p1, p2 in zip(base_blocks[:-1], base_blocks[1:]):
        y0, y1 = p2['value']
        ly0, ly1 = p1['value']
        if DRAW_HEIGHT_BETWEEN_BLOCKS:
            draw.text(
                (0, y0 - 30),
                f'{y0 - ly1}↑',
                font=FONT,
                fill='magenta',
                stroke_width=1
            )


def checkHeadType(img, block: Block):
    w, h = img.size
    y0, y1 = block['value']
    x0, x1 = (MIN_BLUE_X, MAX_BLUE_X)
    data = np.array(img)[y0:y1, x0:x1] / 255

    val = np.apply_along_axis(is_point_blue, -1, data).mean()
    if val > MIN_BLOCK_IS_PROBLEM_PCT:
        return HeadType.PROBLEM

    if (1 - data).mean() < .05:
        # 大标题还需要从中间去确定
        data2 = np.array(img.convert('L'))[y0:y1, int(.4 * w):int(.6 * w)]
        big_title_gray = np.where(data2 > 250, 255, data2).mean()
        if big_title_gray > 200:
            return HeadType.CONTINUE

    return HeadType.TITLE
