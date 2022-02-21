from typing import List

from boa3.neo.vm.type.String import String
from test_runner.neoxp.command import neoxp
from test_runner.neoxp.command.neoexpresscommand import NeoExpressCommand
from test_runner.neoxp.neoinvoke import NeoInvoke


class NeoExpressBatch:
    def __init__(self):
        self._instructions: List[NeoExpressCommand] = []

    def create_neo_express_checkpoint(self, checkpoint_path: str, overwrite: bool = False):
        self._instructions.append(neoxp.create_checkpoint(checkpoint_path, force=overwrite))

    def deploy_contract(self, nef_path: str):
        self._instructions.append(neoxp.contract.deploy(nef_path, 'genesis'))

    def run_contract(self, invoke: NeoInvoke):
        self._instructions.append(neoxp.contract.run(invoke.contract, invoke.operation, *invoke.args,
                                                     account=invoke.invoker))

    def mint_block(self, block_count: int):
        self._instructions.append(neoxp.fastfwd(block_count))

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
