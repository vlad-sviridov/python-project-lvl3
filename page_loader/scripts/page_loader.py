#!/usr/bin/env python3
import sys

from page_loader import logging
from page_loader.cli import arg_parser
from page_loader.loader import download


def main():
    logging.setup()
    parser = arg_parser()
    args = parser.parse_args()
    try:
        output_dir = download(args.url, args.output)
    except Exception as e:
        import logging as logger
        logger.error('Download failed %s', e)
        logger.debug('Get parametrs url=%s, dir=%s', args.url,
                     args.output, exc_info=True)
        sys.exit(1)
    else:
        print(f'Page was successfully downloaded into {output_dir}')


if __name__ == '__main__':
    main()
