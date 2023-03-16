from typing import Dict, Union

from boa3_test.test_drive.neoxp.command import utils
from boa3_test.test_drive.neoxp.command.neoexpresscommand.show.ishowcommand import IShowCommand


class ShowBlockCommand(IShowCommand):
    def __init__(self, block_hash_or_index: Union[bytes, str, int] = None,
                 neo_express_data_file: str = None):

        if isinstance(block_hash_or_index, int) and block_hash_or_index < 0:
            block_hash_or_index = 0

        if isinstance(block_hash_or_index, bytes):
            block_hash_or_index = utils.to_hex_str(block_hash_or_index)

        arguments = []
        if isinstance(block_hash_or_index, (str, int)):
            arguments.append(str(block_hash_or_index))
            hash_or_index = block_hash_or_index
        else:
            hash_or_index = None

        self.block_hash_or_index = hash_or_index
        self.input = neo_express_data_file

        super().__init__('block', arguments)

    def _get_options(self) -> Dict[str, str]:
        return super()._get_options()
