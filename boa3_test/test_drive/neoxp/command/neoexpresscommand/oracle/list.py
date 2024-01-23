from boa3_test.test_drive.neoxp.command.neoexpresscommand.oracle.ioraclecommand import IOracleCommand


class OracleListCommand(IOracleCommand):
    def __init__(self,
                 neo_express_data_file: str = None):

        self.input = neo_express_data_file

        command_id = 'list'

        super().__init__(command_id)

    def _get_options(self) -> dict[str, str]:
        return super()._get_options()
