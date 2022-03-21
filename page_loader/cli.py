import argparse
import os
from typing import Tuple


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='output directory',
        default=os.getcwd(),
    )
    parser.add_argument(
        'url',
        type=str,
        help='web page address'
    )

    return parser


def parse_args() -> Tuple:
    parser = get_parser()
    args = parser.parse_args()
    if os.path.isabs(args.output):
        path = os.path.join(os.getcwd(), args.output)
    else:
        path = args.output

    return (args.url, path)
