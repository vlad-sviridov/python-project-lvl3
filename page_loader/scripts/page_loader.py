#!/usr/bin/env python3
import logging
import sys

import page_loader.logging
from page_loader.cli import get_parser
from page_loader.loader import download


def main():
    page_loader.logging.setup()
    parser = get_parser()
    args = parser.parse_args()
    try:
        output_dir = download(args.url, args.output)
    except Exception as e:
        logging.error('Download failed %s', e)
        logging.debug('Get parametrs url=%s, dir=%s', args.url, args.output)
        sys.exit(1)
    else:
        print('Page was successfully downloaded into %s', output_dir)


if __name__ == '__main__':
    main()
