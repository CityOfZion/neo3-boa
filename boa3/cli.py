import argparse
import logging
import os
import sys

from boa3.boa3 import Boa3
from boa3.internal.exception.NotLoadedException import NotLoadedException


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help=".py smart contract to compile")
    parser.add_argument("-db", "--debug", action='store_true', help="generates a .nefdbgnfo file")
    parser.add_argument("--project-path", help="Project root path. Path of the contract by default.", type=str)
    args = parser.parse_args()

    if not args.input.endswith(".py") or not os.path.isfile(args.input):
        logging.error("Input file is not .py")
        sys.exit(1)

    fullpath = os.path.realpath(args.input)
    path, filename = os.path.split(fullpath)

    if not args.project_path:
        args.project_path = os.path.dirname(path)

    try:
        Boa3.compile_and_save(args.input, debug=args.debug, root_folder=args.project_path)
        logging.info(f"Wrote {filename.replace('.py', '.nef')} to {path}")
    except NotLoadedException as e:
        error_message = e.message
        log_error = 'Could not compile'
        if len(error_message) > 0:
            log_error += f': {error_message}'

        logging.error(log_error)
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    main()
