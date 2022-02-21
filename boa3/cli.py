import argparse
import logging
import os
import sys

from boa3.boa3 import Boa3
from boa3.exception.NotLoadedException import NotLoadedException


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help=".py smart contract to compile")
    parser.add_argument("-db", "--debug", action='store_true', help="generates a nefdbgnfo file")
    args = parser.parse_args()

    if not args.input.endswith(".py") or not os.path.isfile(args.input):
        logging.error("Input file is not .py")
        sys.exit(1)

    fullpath = os.path.realpath(args.input)
    path, filename = os.path.split(fullpath)

    try:
        Boa3.compile_and_save(args.input, debug=args.debug)
        logging.info(f"Wrote {filename.replace('.py', '.nef')} to {path}")
    except NotLoadedException as e:
        logging.error("Could not compile")
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    main()
