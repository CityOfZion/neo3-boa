from typing import List

from boa3.neo.vm.type.String import String
from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.neoxp import utils
from boa3_test.test_drive.neoxp.command import neoxp, neoxp_contract
from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand


class NeoExpressBatch:
    def __init__(self):
        self._instructions: List[NeoExpressCommand] = []

    def is_empty(self) -> bool:
        return len(self._instructions) == 0

    def cur_size(self) -> int:
        return len(self._instructions)

    def create_neo_express_checkpoint(self, checkpoint_path: str, overwrite: bool = False):
        self._instructions.append(neoxp.create_checkpoint(checkpoint_path, force=overwrite))

    def deploy_contract(self, nef_path: str) -> TestContract:
        self._instructions.append(neoxp_contract.deploy(nef_path, 'genesis'))
        return TestContract(nef_path, nef_path.replace('.nef', '.manifest.json'))

    def run_contract(self, invoke: NeoInvoke):
        self._instructions.append(neoxp_contract.run(invoke.contract, invoke.operation, *invoke.args,
                                                     account=invoke.invoker))

    def mint_block(self, block_count: int):
        self._instructions.append(neoxp.fastfwd(block_count))

    def reset_blockchain(self):
        self._instructions.append(neoxp.reset())

    def clear(self):
        self._instructions.clear()

    def pop(self):
        return self._instructions.pop()

    def write(self, path: str) -> bool:
        try:
            with open(path, 'wb+') as json_file:
                for instruction in self._instructions:
                    json_file.write(String(f'{instruction.cli_command()}\n').to_bytes())

            return True
        except BaseException:
            return False

    def execute(self, neoxp_path: str, batch_file_path: str, reset: bool = False):
        self.write(batch_file_path)
        utils.run_batch(neoxp_path, batch_file_path, reset=reset)

    def has_new_deploys_since(self, last_verified_command: int = -1):
        if not isinstance(last_verified_command, int):
            last_verified_command = -1

        return next((True for command in self._instructions[last_verified_command + 1:]
                     if command.is_command("contract deploy")),
                    False)
