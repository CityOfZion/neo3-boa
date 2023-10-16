import abc
from typing import Dict, List


class NeoExpressCommand:
    def __init__(self, command_id: str, args: List[str] = None, options: Dict[str, str] = None):
        if not isinstance(args, list):
            args = []

        if not isinstance(options, dict):
            options = self._get_options()

        self._command_id = command_id
        self._args = args
        self._options = options

    @abc.abstractmethod
    def _get_options(self) -> Dict[str, str]:
        import os.path
        options = {}

        if hasattr(self, 'input') and isinstance(self.input, str) and os.path.isfile(self.input):
            options['--input'] = self.input

        return options

    def cli_command(self) -> str:
        command = [self._command_id]

        for o in self._options.items():
            command.extend(o)

        for arg in self._args:
            command.append(arg)

        return ' '.join(command)

    def is_command(self, command: str) -> bool:
        if not isinstance(command, str) or len(command) == 0:
            return True

        sep = ' '
        args = command.split(sep)
        command_id_split_size = len(self._command_id.split(sep))
        command_id = sep.join(args[:command_id_split_size])
        if command_id != self._command_id:
            return False

        args = args[command_id_split_size:]
        args_compare_size = len(args)
        if args_compare_size == 0:
            return True
        if args_compare_size > len(self._args):
            return False
        return self._args[:args_compare_size] == args

    def __str__(self) -> str:
        return self._command_id
