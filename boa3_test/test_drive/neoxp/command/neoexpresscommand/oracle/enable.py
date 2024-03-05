from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command.neoexpresscommand.oracle.ioraclecommand import IOracleCommand


class OracleEnableCommand(IOracleCommand):
    def __init__(self, account: Account,
                 trace: bool = False,
                 neo_express_data_file: str = None):

        self.trace = trace
        self.input = neo_express_data_file

        command_id = 'enable'
        args = [
            account.get_identifier(),
        ]

        super().__init__(command_id, args)

    def _get_options(self) -> dict[str, str]:
        options = super()._get_options()

        if self.trace:
            options['--trace'] = ''

        return options
