import os

import argparse


def arg_parser():
    parser = argparse.ArgumentParser(
        description='page-loader is cli for download a web-page'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='output directory (default: current directory)',
        default=os.getcwd(),
    )
    parser.add_argument(
        'url',
        type=str,
        help='web page address'
    )

    return parser
