"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 09, 2022, 13:02
"""

# 确定题目的标题蓝色位置
MIN_BLUE_X = 100
MAX_BLUE_X = 400

# .05 第24张通不过，大多数都可以
# 这个参数和 M{XX}_BLUE_X 关系很大
MIN_BLOCK_IS_PROBLEM_PCT = .01

# 一个区块的最小高度，低于这个高度的可能是有噪点的空白行
# 如果有些分子分母被该参数排除了，问题不大，可以输出时基于 padding 解决
MIN_BLOCK_HEIGHT = 6

# 判定两个区块之间的最小高度差，低于则合并
# 经过验证，无法通过区块之间的高度差区分大题与小题 :(
# 比9低就不能把一些分子分母粘合一起了，不过可以后续再合并
# 比11低就无法合并第29张第1题
MIN_HEIGHT_BETWEEN_BLOCKS = 11

# 没合并正确的基本都是一些游离的分子分母，可以输出时基于 padding 解决
CROP_PADDING_Y = MIN_HEIGHT_BETWEEN_BLOCKS - 1

# 判断一行是否非空白行的最小有效点数
MIN_NON_WHITE_POINTS_IN_ROW = 1

# 保证block的框选是最佳视觉比例
MARGIN_LEFT_PCT = .03

# 去除页面上下部分的空白
TOP_PCT = .05
BOTTOM_PCT = .95

DRAW_BLOCK_TYPE_SQUARE_SIZE = 20

MERGE_CONTOURS = False
DRAW_BLUE_XS = True
DRAW_BLOCK_TYPE = True
DRAW_BLOCK_CONTOUR = True
DRAW_BLOCK_COORDS = False
DRAW_HEIGHT_BETWEEN_BLOCKS = False
SHOW_BLUE_XS_DISTRIBUTION = False
QR_MARGIN = 25
QR_RADIUS = 100
QR_PADDING_LEFT = 10
QR_HALF_SIZE = (QR_MARGIN + QR_RADIUS)
QR_BLUR_MIN = 150
