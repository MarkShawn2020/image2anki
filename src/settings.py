"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 08, 2022, 15:10
"""
import os

SRC_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
PDF_PPI = 300
PDF_IMAGES_RAW_DIR = os.path.join(DATA_DIR, 'images-raw')
PDF_IMAGES_DRAW_DIR = os.path.join(DATA_DIR, 'images-draw')
PDF_PATH = os.path.join(DATA_DIR, '李正元2021考研数学一复习全书pdf高清无水印版彩色版.pdf')
