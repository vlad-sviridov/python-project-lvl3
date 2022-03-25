import argparse
import os


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
