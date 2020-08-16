#!/usr/bin/env python3
"""CLI for pymergevcd - present the options to the user"""

import argparse
import sys

import colorama
from exitstatus import ExitStatus

import pymergevcd.io_manager


def parse_args() -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
        description='Merge given files on command-line.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infiles', metavar='file', type=str, nargs='+',
                        help='Files to be merged')
    parser.add_argument('-o',
                        metavar='out.vcd',
                        type=str,
                        required=False,
                        default='out.vcd',
                        help='Optional output filename')
    return parser.parse_args()


def main() -> ExitStatus:
    """Parse files into one VCD."""
    colorama.init(autoreset=True, strip=False)
    args = parse_args()
    print('Input files:' + colorama.Fore.CYAN + ' ' + str(args.infiles))

    iom = pymergevcd.io_manager.InputOutputManager()
    iom.merge_files(args.infiles, args.o)

    return ExitStatus.success


# Allow the script to be run standalone (useful during development in PyCharm).
if __name__ == '__main__':
    sys.exit(main())
