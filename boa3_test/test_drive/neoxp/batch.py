import threading
from typing import Any

from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.interface.itransactionobject import ITransactionObject
from boa3_test.test_drive.model.invoker.neobatchinvoke import NeoBatchInvoke
from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke
from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp import utils
from boa3_test.test_drive.neoxp.command import neoxp
from boa3_test.test_drive.neoxp.command.neoexpresscommand import NeoExpressCommand

_NEOXP_BATCH_LOCK = threading.Lock()


class NeoExpressBatch:
    def __init__(self, neoxp_config):
        self._instructions: list[NeoExpressCommand] = []
        self._transaction_submissions: list[int] = []
        self._transaction_logs: list[str] = []

        self._tx_invokes: list[ITransactionObject] = []
        self._tx_invokes_pos: list[int] = []
        self._neoxp_config = neoxp_config

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
            deployer_id = utils.get_default_account(self._neoxp_config)  # neo express default account

        tx_pos = len(self._instructions)
        deployed_contract = TestContract(nef_path, nef_path.replace('.nef', '.manifest.json'))

        self._instructions.append(neoxp.contract.deploy(nef_path, deployer_id))
        self._transaction_submissions.append(tx_pos)

        self._tx_invokes.append(deployed_contract)
        self._tx_invokes_pos.append(tx_pos)

        return deployed_contract

    def run_contract(self, invoke: NeoInvoke, witness_scope: WitnessScope = None,
                     expected_result_type: type = None) -> NeoBatchInvoke:
        if hasattr(invoke.invoker, 'name') and isinstance(invoke.invoker.name, str):
            invoker_id = invoke.invoker
        else:
            invoker_id = utils.get_default_account(self._neoxp_config)  # neo express default account

        tx_pos = len(self._instructions)
        batch_invoke = NeoBatchInvoke(invoke, tx_pos, expected_result_type=expected_result_type)

        self._instructions.append(neoxp.contract.run(invoke.contract_id, invoke.operation, *invoke.cli_args,
                                                     account=invoker_id, witness_scope=witness_scope))
        self._transaction_submissions.append(tx_pos)

        self._tx_invokes.append(batch_invoke)
        self._tx_invokes_pos.append(tx_pos)

        return batch_invoke

    def invoke_file(self, invoke_file: str, account: Account = None, witness_scope: WitnessScope = None):
        if hasattr(account, 'name') and isinstance(account.name, str):
            invoker_id = account
        else:
            invoker_id = utils.get_default_account(self._neoxp_config)  # neo express default account

        if witness_scope != WitnessScope.CalledByEntry:
            # only CalledByEntry and Global are accepted as WitnessScopes in neo express
            witness_scope = WitnessScope.Global

        self._instructions.append(neoxp.contract.invoke(invoke_file, invoker_id, witness_scope))

    def transfer_assets(self, sender: Account, receiver: Account, asset: str | UInt160,
                        quantity: int | float, decimals: int = 0, data: Any = None):
        if isinstance(asset, UInt160):
            asset = asset.__str__()

        self._instructions.append(neoxp.transfer(sender, receiver, asset,
                                                 quantity, decimals=decimals,
                                                 data=data)
                                  )

    def mint_block(self, block_count: int, time_interval_in_secs: int = 0):
        self._instructions.append(neoxp.fastfwd(block_count, time_interval_in_secs))

    def reset_blockchain(self):
        self._instructions.append(neoxp.reset())

    def clear(self):
        self._instructions.clear()
        self._transaction_submissions.clear()
        self._transaction_logs.clear()
        self._tx_invokes.clear()
        self._tx_invokes_pos.clear()

    def pop(self):
        result = self._instructions.pop()

        pop_index = len(self._instructions)
        if pop_index in self._transaction_submissions:
            index = self._transaction_submissions.index(len(self._instructions))
            self._transaction_submissions.pop(index)
            if len(self._transaction_logs) > index:
                self._transaction_logs.pop(index)
        if pop_index in self._tx_invokes_pos:
            index = self._tx_invokes_pos.index(len(self._instructions))
            self._tx_invokes_pos.pop(index)
            self._tx_invokes.pop(index)

        return result

    def write(self, path: str) -> bool:
        try:
            with open(path, 'wb+') as json_file:
                for instruction in self._instructions:
                    json_file.write(String(f'{instruction.cli_command()}\n').to_bytes())

            return True
        except BaseException:
            return False

    def execute(self, neoxp_path: str, batch_file_path: str, reset: bool = False, check_point_file: str = None) -> str:
        with _NEOXP_BATCH_LOCK:
            self.write(batch_file_path)
            log = self._run_batch(neoxp_path, batch_file_path, reset=reset, check_point_file=check_point_file)

        self._transaction_logs.clear()
        self._update_logs(log)
        self._remove_commands_until_checkpoint(check_point_file)
        return log

    def _run_batch(self, neoxp_path: str, batch_file_path: str, reset: bool = False, check_point_file: str = None):
        return utils.run_batch(neoxp_path, batch_file_path, reset=reset, check_point_file=check_point_file)

    def _update_logs(self, log: str):
        import re
        cli_color_change = r'\xb1?(?:\[\d+m)?'
        log_regex = rf'{cli_color_change}(?P<contract>.+?){cli_color_change}\sLog:\s{cli_color_change}'
        tx_logs = []

        # filter to remove logs
        logs = log.splitlines()
        max_log_count = len(self._instructions)

        index = len(logs) - 1
        while index >= 0 and 0 < len(logs) - index <= max_log_count:
            line = logs[index]
            if re.match(log_regex, line):
                logs.pop(index)
            index -= 1

        for lineno, line in enumerate(logs[-max_log_count:]):
            if lineno in self._transaction_submissions:
                tx_logs.append(line)
            if lineno in self._tx_invokes_pos:
                index = self._tx_invokes_pos.index(lineno)
                self._tx_invokes[index].set_log(line)

        self._transaction_logs = tx_logs

    def _remove_commands_until_checkpoint(self, check_point_file: str):
        if isinstance(check_point_file, str):
            condition = (index + 1 for index, command in enumerate(self._instructions)
                         if (isinstance(command, neoxp.neoxp.checkpoint.CheckpointCreateCommand)
                             and command.file_name == check_point_file
                             )
                         )
        else:
            condition = (index + 1 for index, command in enumerate(self._instructions)
                         if isinstance(command, neoxp.neoxp.checkpoint.CheckpointCreateCommand)
                         )

        instr_to_remove = next(condition, None)
        if isinstance(instr_to_remove, int):
            self._instructions[:instr_to_remove] = []

            last_tx_submitted = next((index for index, tx_pos in enumerate(self._transaction_submissions)
                                      if tx_pos > instr_to_remove
                                      ), len(self._transaction_submissions))
            last_sc_submitted = next((index for index, tx_pos in enumerate(self._tx_invokes_pos)
                                      if tx_pos > instr_to_remove
                                      ), len(self._tx_invokes))

            self._transaction_logs[:last_tx_submitted] = []
            self._transaction_submissions[:last_tx_submitted] = []
            self._tx_invokes[:last_sc_submitted] = []
            self._tx_invokes_pos[:last_sc_submitted] = []

    def has_new_deploys(self):
        return next((True for command in self._instructions
                     if isinstance(command, neoxp.neoxp.contract.deploy.ContractDeployCommand)),
                    False)

    def oracle_enable(self, account: Account):
        self._instructions.append(neoxp.oracle.enable(account)
                                  )

    def oracle_response(self, url: str, response_path: str, request_id: int = None):
        self._instructions.append(neoxp.oracle.response(url, response_path,
                                                        request_id=request_id))
