import abc
from typing import List

from boa3_test.test_drive.neoxp.command.neoexpresscommand.neoexpresscommand import NeoExpressCommand


class IContractCommand(abc.ABC, NeoExpressCommand):
    def __init__(self, sub_command_id: str, args: List[str] = None):
        command_id = 'contract'
        if len(sub_command_id) > 0:
            command_id = f'{command_id} {sub_command_id}'

        super().__init__(command_id, args)
