import json
from typing import Dict, Any

from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp.command import utils
from boa3_test.test_drive.neoxp.command.neoexpresscommand.neoexpresscommand import NeoExpressCommand

__all__ = ['TransferAssetCommand']


class TransferAssetCommand(NeoExpressCommand):
    def __init__(self, token_symbol: str, sender: Account, receiver: Account, quantity: float,
                 data: Any = None,
                 trace: bool = False,
                 decimals: int = 0,
                 neo_express_data_file: str = None):

        self.token_symbol = token_symbol
        self.sender = sender
        self.receiver = receiver
        self.quantity = quantity

        self.data = data
        self.trace = trace
        self.input = neo_express_data_file

        if decimals < 0:
            decimals = 0

        command_id = 'transfer'
        args = [
            utils.stringify_asset_quantity(quantity, decimals),
            token_symbol,
            sender.get_identifier(),
            receiver.get_identifier(),
        ]

        super().__init__(command_id, args)

    def _get_options(self) -> Dict[str, str]:
        options = super()._get_options()

        if self.data is not None:
            options['--data'] = json.dumps(self.data)
        if self.trace:
            options['--trace'] = ''

        return options
