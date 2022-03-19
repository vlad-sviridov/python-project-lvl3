#!/usr/bin/env python
from page_loader.cli import parse_args
from page_loader.loader import download


def main():
    args = parse_args()
    output_dir = download(args[0], args[1])
    print(output_dir)


if __name__ == '__main__':
    main()
