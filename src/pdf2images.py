"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 08, 2022, 15:10
"""
import os
from typing import List

from PIL import Image
from pdf2image import convert_from_path

from src.settings import PDF_PPI, PDF_IMAGES_RAW_DIR, PDF_PATH


def pdf2images(fp: str, ppi=PDF_PPI):
    print(f'converting file://{fp}, ppi={ppi}')
    pages: List[Image] = convert_from_path(
        fp,
        thread_count=12,
        dpi=ppi,
        fmt='jpeg',
    )
    n = len(pages)
    for i in range(n):
        page = pages[i]  # type: Image
        print(f'saving [{i + 1}/{n}]')
        page.save(os.path.join(PDF_IMAGES_RAW_DIR, f'{i + 1}.jpg'), 'JPEG')


if __name__ == '__main__':
    pdf2images(PDF_PATH)
