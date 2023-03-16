from typing import Dict, Union

from boa3_test.test_drive.neoxp.command import utils
from boa3_test.test_drive.neoxp.command.neoexpresscommand.show.ishowcommand import IShowCommand


class ShowTransactionCommand(IShowCommand):
    def __init__(self, transaction_hash: Union[bytes, str],
                 neo_express_data_file: str = None):

        if isinstance(transaction_hash, bytes):
            transaction_hash = utils.to_hex_str(transaction_hash)

        self.transaction_hash = transaction_hash
        self.input = neo_express_data_file

        super().__init__('transaction', [transaction_hash])

    def _get_options(self) -> Dict[str, str]:
        return super()._get_options()
