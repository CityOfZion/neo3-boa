from typing import Dict, List


class NeoExpressCommand:
    def __init__(self, command_id: str, args: List[str] = None, options: Dict[str, str] = None):
        if not isinstance(args, list):
            args = []

        if not isinstance(options, dict):
            options = {}

        self._command_id = command_id
        self._args = args
        self._options = options

    def cli_command(self) -> str:
        command = [self._command_id]

        for o in self._options.items():
            command.extend(o)

        command.extend(self._args)

        return ' '.join(command)

    def __str__(self) -> str:
        return self._command_id
