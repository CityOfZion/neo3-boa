from typing import Dict

from boa3_test.test_drive.neoxp.command.neoexpresscommand.neoexpresscommand import NeoExpressCommand

__all__ = ['FastForwardCommand']


class FastForwardCommand(NeoExpressCommand):
    def __init__(self, block_count: int = 0,
                 time_interval_in_secs: int = 0,
                 neo_express_data_file: str = None):

        self.block_count = block_count if block_count > 0 else 0
        self.timestamp_delta = time_interval_in_secs if time_interval_in_secs > 0 else 0
        self.input = neo_express_data_file

        command_id = 'fastfwd'
        args = []
        if isinstance(block_count, int):
            args.append(str(block_count))

        super().__init__(command_id, args)

    def _get_options(self) -> Dict[str, str]:
        options = super()._get_options()

        if self.timestamp_delta > 0:
            options['--timestamp-delta'] = str(self.timestamp_delta)

        return options
