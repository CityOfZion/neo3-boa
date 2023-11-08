import logging
import os
import sys
from argparse import _SubParsersAction
from typing import Optional

from boa3.boa3 import Boa3
from boa3.internal.cli_commands.icommand import ICommand
from boa3.internal.exception.NotLoadedException import NotLoadedException


class CompileCommand(ICommand):

    def __init__(self, main_parser: _SubParsersAction):
        super().__init__(main_parser, 'compile', 'Compiles your smart contract')

    def add_arguments_and_callback(self):
        self.parser.add_argument("input",
                                 type=str,
                                 help=".py smart contract to compile")
        self.parser.add_argument("-db", "--debug",
                                 action='store_true',
                                 help="generates a .nefdbgnfo file")
        self.parser.add_argument("--project-path",
                                 type=str,
                                 help="Project root path. Path of the contract by default.")
        self.parser.add_argument("-e", "--env",
                                 type=str,
                                 help="Set the contract environment for compiling.")
        self.parser.add_argument("-o", "--output-path",
                                 metavar='NEF_OUTPUT',
                                 type=str,
                                 default=None,
                                 help="Chooses the name and where the compiled files will be generated, "
                                      "if not specified it will be generated on the same directory with the same name "
                                      "as the python file.")
        self.parser.add_argument("--no-failfast",
                                 action='store_true',
                                 help="Do not stop on first compile error")
        self.parser.add_argument("--log-level",
                                 type=str,
                                 help="Log output level")

        self.parser.set_defaults(func=self.execute_command)

    @staticmethod
    def execute_command(args: dict):
        sc_path: str = args['input']
        project_path: str = args['project_path']
        debug: bool = args['debug']
        env: str = args['env']
        output_path: Optional[str] = args['output_path']
        fail_fast: bool = not args['no_failfast']
        log_level = args['log_level']

        if not sc_path.endswith(".py") or not os.path.isfile(sc_path):
            logging.error("Input file is not .py")
            sys.exit(1)

        fullpath = os.path.realpath(sc_path)
        path, filename = os.path.split(fullpath)

        if isinstance(output_path, str):
            if not output_path.endswith('.nef'):
                logging.error("Output path file extension is not .nef")
                sys.exit(1)

            path, filename = os.path.split(os.path.realpath(output_path))

        try:
            Boa3.compile_and_save(sc_path,
                                  output_path=output_path,
                                  debug=debug,
                                  root_folder=project_path,
                                  env=env,
                                  fail_fast=fail_fast,
                                  show_errors=True,
                                  log_level=log_level
                                  )
            logging.info(f"Wrote {filename.replace('.py', '.nef')} to {path}")
        except NotLoadedException as e:
            error_message = e.message
            log_error = 'Could not compile'
            if len(error_message) > 0:
                log_error += f': {error_message}'

            logging.error(log_error)
            sys.exit(1)
        except Exception as e:
            logging.exception(e)
            sys.exit(1)
