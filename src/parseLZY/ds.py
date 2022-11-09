"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 09, 2022, 12:55
"""
from enum import Enum
from typing import TypedDict, Tuple

from PIL import ImageFont


class HeadType(int, Enum):
    PROBLEM = 0  # blue
    TITLE = 1  # black
    CONTINUE = 2  # white


HeadTypeColorMap = {
    HeadType.PROBLEM : 'blue',
    HeadType.TITLE   : 'gray',
    HeadType.CONTINUE: 'green',
}


class BaseBlock(TypedDict):
    # [i, j)
    value: Tuple[int]


class Block(BaseBlock):
    head: HeadType


FONT = ImageFont.truetype(font='/System/Library/Fonts/PingFang.ttc', size=30)