#!/usr/bin/env python
# coding: utf-8

import argparse

from launchctl_py.create import create
from launchctl_py.status import status

from launchctl_py.create import create
from launchctl_py.status import status


def _opts() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c",
                        "--create",
                        help="Create a new launchctl agent",
                        action="store_true")
    parser.add_argument("-s",
                        "--status",
                        help="Get the status of the agents you created",
                        action="store_true")
    return parser


def main():
    opts = _opts().parse_args()
    if opts.create:
        create()
    elif opts.status:
        print(status())
    else:
        _opts().print_help()


if __name__ == "__main__":
    main()
