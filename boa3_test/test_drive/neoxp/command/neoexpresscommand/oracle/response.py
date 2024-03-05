from boa3_test.test_drive.neoxp.command.neoexpresscommand.oracle.ioraclecommand import IOracleCommand


class OracleResponseCommand(IOracleCommand):
    def __init__(self, url: str, response_path: str,
                 request_id: int | None = None,
                 trace: bool = False,
                 neo_express_data_file: str = None):

        self.request_id = request_id
        self.trace = trace
        self.input = neo_express_data_file

        command_id = 'response'
        args = [
            url,
            response_path,
        ]

        super().__init__(command_id, args)

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if self.request_id:
            options[f'--request_id:{self.request_id}'] = ''

        if self.trace:
            options['--trace'] = ''

        return options
