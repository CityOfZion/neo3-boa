from typing import List, Union, Any, Type

from boa3.neo.vm.type.String import String
from boa3.neo3.core.types import UInt160
from boa3_test.test_drive.model.invoker.neobatchinvoke import NeoBatchInvoke
from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp import utils
from boa3_test.test_drive.neoxp.command import neoxp
from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand


class NeoExpressBatch:
    def __init__(self):
        self._instructions: List[NeoExpressCommand] = []
        self._transaction_submissions: List[int] = []
        self._transaction_logs: List[str] = []

        self._contract_invokes: List[NeoBatchInvoke] = []
        self._contract_invokes_pos: List[int] = []

    def is_empty(self) -> bool:
        return len(self._instructions) == 0

    def cur_size(self) -> int:
        return len(self._instructions)

    def create_neo_express_checkpoint(self, checkpoint_path: str, overwrite: bool = False):
        self._instructions.append(neoxp.create_checkpoint(checkpoint_path, force=overwrite))

    def deploy_contract(self, nef_path: str, deployer: Account = None) -> TestContract:
        if hasattr(deployer, 'name') and isinstance(deployer.name, str):
            deployer_id = deployer
        else:
            deployer_id = utils.get_default_account()  # neo express default account

        tx_pos = len(self._instructions)
        self._instructions.append(neoxp.contract.deploy(nef_path, deployer_id))
        self._transaction_submissions.append(tx_pos)

        return TestContract(nef_path, nef_path.replace('.nef', '.manifest.json'))

    def run_contract(self, invoke: NeoInvoke,
                     expected_result_type: Type = None) -> NeoBatchInvoke:
        if hasattr(invoke.invoker, 'name') and isinstance(invoke.invoker.name, str):
            invoker_id = invoke.invoker
        else:
            invoker_id = utils.get_default_account()  # neo express default account

        tx_pos = len(self._instructions)
        batch_invoke = NeoBatchInvoke(invoke, tx_pos, expected_result_type=expected_result_type)

        self._instructions.append(neoxp.contract.run(invoke.contract_id, invoke.operation, *invoke.args,
                                                     account=invoker_id))
        self._transaction_submissions.append(tx_pos)

        self._contract_invokes.append(batch_invoke)
        self._contract_invokes_pos.append(tx_pos)

        return batch_invoke

    def transfer_assets(self, sender: Account, receiver: Account, asset: Union[str, UInt160],
                        quantity: Union[int, float], decimals: int = 0, data: Any = None):
        if isinstance(asset, UInt160):
            asset = asset.__str__()

        self._instructions.append(neoxp.transfer(sender, receiver, asset,
                                                 quantity, decimals=decimals,
                                                 data=data)
                                  )

    def mint_block(self, block_count: int):
        self._instructions.append(neoxp.fastfwd(block_count))

    def reset_blockchain(self):
        self._instructions.append(neoxp.reset())

    def clear(self):
        self._instructions.clear()
        self._transaction_submissions.clear()
        self._transaction_logs.clear()

    def pop(self):
        result = self._instructions.pop()

        pop_index = len(self._instructions)
        if pop_index in self._transaction_submissions:
            index = self._transaction_submissions.index(len(self._instructions))
            self._transaction_submissions.pop(index)
            if len(self._transaction_logs) > index:
                self._transaction_logs.pop(index)

        return result

    def write(self, path: str) -> bool:
        try:
            with open(path, 'wb+') as json_file:
                for instruction in self._instructions:
                    json_file.write(String(f'{instruction.cli_command()}\n').to_bytes())

            return True
        except BaseException:
            return False

    def execute(self, neoxp_path: str, batch_file_path: str, reset: bool = False) -> str:
        self.write(batch_file_path)
        self._transaction_logs.clear()
        log = utils.run_batch(neoxp_path, batch_file_path, reset=reset)

        self._update_logs(log)
        return log

    def _update_logs(self, log: str):
        tx_logs = []
        for lineno, line in enumerate(log.splitlines()[-len(self._instructions):]):
            if lineno in self._transaction_submissions:
                tx_logs.append(line)
            if lineno in self._contract_invokes_pos:
                index = self._contract_invokes_pos.index(lineno)
                self._contract_invokes[index]._log = line
        self._transaction_logs = tx_logs

    def has_new_deploys_since(self, last_verified_command: int = -1):
        if not isinstance(last_verified_command, int):
            last_verified_command = -1

        return next((True for command in self._instructions[last_verified_command + 1:]
                     if command.is_command("contract deploy")),
                    False)
