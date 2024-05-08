from boa3_test.test_drive.neoxp.command.neoexpresscommand.neoexpresscommand import NeoExpressCommand

__all__ = ['BatchCommand']


class BatchCommand(NeoExpressCommand):
    def __init__(self, file_name: str,
                 reset: bool = False,
                 check_point_file: str | None = None,
                 trace: bool = False,
                 neo_express_data_file: str = None):

        self.file_name = file_name
        self.reset = reset
        self.check_point_file = check_point_file
        self.trace = trace
        self.input = neo_express_data_file

        command_id = 'batch'
        super().__init__(command_id, [file_name])

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if self.reset or isinstance(self.check_point_file, str):
            flag = '--reset'
            if isinstance(self.check_point_file, str):
                flag = f'{flag}:{self.check_point_file}'

            options[flag] = ''
        if self.trace:
            options['--trace'] = ''

        return options
