"""
source: own
author: https://github.com/MarkShawn2020
create: Nov 08, 2022, 14:56
"""

from argparse import ArgumentParser

from src.pdf2images import pdf2images

from src.split_problems import splitProblems


if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_pdf2images = subparsers.add_parser('pdf2images')
    parser_pdf2images.add_argument('fp', help='pdf文档，本项目目前使用的是2021年李正元复习全书数学一习题册')
    parser_pdf2images.set_defaults(func=lambda x: pdf2images(fp=x.fp))

    parser_split_problems = subparsers.add_parser('split-problems')
    parser_split_problems.add_argument('fp', help='李正元习题册某一页的图片文件地址，在 data/images 下')
    parser_split_problems.set_defaults(func=lambda x: splitProblems(fp=x.fp))

    args = parser.parse_args()
    args.func(args)
