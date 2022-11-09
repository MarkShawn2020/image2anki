"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 08, 2022, 21:24
"""

import os.path

from PIL import Image

from src.parseLZY.utils import dropQrCode, getBaseBlocks, doDraw, checkHeadType
from src.settings import PDF_IMAGES_RAW_DIR, PDF_IMAGES_DRAW_DIR


class BaseParser:

    def __init__(self, fp):
        self._fp = fp
        self._img = Image.open(self._fp)

    def run(self, save=True, show=True):
        print(f'handling file://{self._fp}')

        dropQrCode(self._img)
        base_blocks = getBaseBlocks(self._img)
        for block in base_blocks:
            block['headType'] = checkHeadType(self._img, block)
        doDraw(self._img, base_blocks)
        if show:
            self._img.show()
        if save:
            fn = os.path.basename(self._fp)
            fp_out = os.path.join(PDF_IMAGES_DRAW_DIR, fn)
            print(f'saving into file://{fp_out}')
            self._img.save(fp_out)


class AnswerParser(BaseParser):

    def __init__(self, fp, *args, **kwargs):
        super().__init__(fp)


if __name__ == '__main__':
    BaseParser(os.path.join(PDF_IMAGES_RAW_DIR, f'lzy-{59:03d}.jpg')).run()

    # for page in range(5, 53): splitProblems(os.path.join(PDF_IMAGES_RAW_DIR, f'lzy-{page:03d}.jpg'))
