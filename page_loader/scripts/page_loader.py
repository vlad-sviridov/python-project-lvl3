#!/usr/bin/env python3
import logging
import logging.config
import sys

from page_loader.cli import get_parser
from page_loader.loader import download
from page_loader.logging import setup


def main():
    setup()
    parser = get_parser()
    args = parser.parse_args()
    try:
        output_dir = download(args.url, args.output)
    except Exception as e:
        logging.error('Download failed %s', e)
        sys.exit(1)
    else:
        print(f'Page was successfully downloaded into {output_dir}')


if __name__ == '__main__':
    main()
