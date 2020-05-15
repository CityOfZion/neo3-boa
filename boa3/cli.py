import argparse
import sys
import os
from boa3.boa3 import Boa3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help=".py smart contract to compile")
    args = parser.parse_args()

    if not args.input.endswith(".py") or not os.path.isfile(args.input):
        print("Input file is not .py")
        sys.exit(1)

    fullpath = os.path.realpath(args.input)
    path, filename = os.path.split(fullpath)

    try:
        Boa3.compile_and_save(args.input)
        print(f"Wrote {filename.replace('.py', '.nef')} to {path}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
