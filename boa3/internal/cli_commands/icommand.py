from abc import ABC, abstractmethod
from argparse import ArgumentParser, _SubParsersAction


class ICommand(ABC):

    def __init__(self, main_parser: _SubParsersAction, command_name: str, help_text: str):
        self.parser: ArgumentParser = main_parser.add_parser(command_name, help=help_text)

    @abstractmethod
    def add_arguments_and_callback(self):
        pass

    @staticmethod
    @abstractmethod
    def execute_command(args: dict):
        pass
