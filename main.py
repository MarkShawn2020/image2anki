"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 08, 2022, 14:56
"""

from src.pdf2images import pdf2images
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--pdf2images')
    parser.add_argument('--pdf-path')
    args = parser.parse_args()

    if args.pdf2images():
        pdf2images(args.pdf_path)
