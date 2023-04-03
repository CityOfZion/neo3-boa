import logging
import os
import sys
from argparse import _SubParsersAction

from boa3.boa3 import Boa3
from boa3.internal.cli_commands.icommand import ICommand
from boa3.internal.exception.NotLoadedException import NotLoadedException


class BuildCommand(ICommand):

    def __init__(self, main_parser: _SubParsersAction):
        super().__init__(main_parser, 'compile', 'Compiles your smart contract')

    def add_arguments_and_callback(self):
        self.parser.add_argument("input", help=".py smart contract to compile", type=str)
        self.parser.add_argument("-db", "--debug", action='store_true', help="generates a .nefdbgnfo file")
        self.parser.add_argument("--project-path", help="Project root path. Path of the contract by default.", type=str)
        self.parser.set_defaults(func=self.execute_command)

    @staticmethod
    def execute_command(args: dict):
        sc_path: str = args['input']
        project_path: str = args['project_path']
        debug: bool = args['debug']

        if not sc_path.endswith(".py") or not os.path.isfile(sc_path):
            logging.error("Input file is not .py")
            sys.exit(1)

        fullpath = os.path.realpath(sc_path)
        path, filename = os.path.split(fullpath)

        if not project_path:
            project_path = os.path.dirname(path)

        try:
            Boa3.compile_and_save(sc_path, debug=debug, root_folder=project_path)
            logging.info(f"Wrote {filename.replace('.py', '.nef')} to {path}")
        except NotLoadedException as e:
            error_message = e.message
            log_error = 'Could not compile'
            if len(error_message) > 0:
                log_error += f': {error_message}'

            logging.error(log_error)
        except Exception as e:
            logging.exception(e)
