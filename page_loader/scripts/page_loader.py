#!/usr/bin/env python
from page_loader.cli import get_parser
from page_loader.loader import download


def main():
    parser = get_parser()
    args = parser.parse_args()
    output_dir = download(args.url, args.output)
    print(output_dir)


if __name__ == '__main__':
    main()
