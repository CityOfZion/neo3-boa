__all__ = [
    'NeoTestRunner'
]

import json
import os.path
import subprocess
from collections.abc import Callable, Sequence
from typing import Any

from boa3.internal import constants
from boa3.internal.neo import utils as neo_utils
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.core.types import UInt256
from boa3.internal.neo3.vm import vmstate, VMState
from boa3_test.test_drive.model.invoker.neobatchinvoke import NeoBatchInvoke
from boa3_test.test_drive.model.invoker.neoinvokecollection import NeoInvokeCollection
from boa3_test.test_drive.model.invoker.neoinvokeresult import NeoInvokeResult
from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp import utils as neoxp_utils
from boa3_test.test_drive.neoxp.batch import NeoExpressBatch
from boa3_test.test_drive.neoxp.model.neoxpconfig import NeoExpressConfig
from boa3_test.test_drive.testrunner import utils
from boa3_test.test_drive.testrunner.blockchain.block import TestRunnerBlock as Block
from boa3_test.test_drive.testrunner.blockchain.log import TestRunnerLog as Log
from boa3_test.test_drive.testrunner.blockchain.notification import TestRunnerNotification as Notification
from boa3_test.test_drive.testrunner.blockchain.storage import TestRunnerStorage as Storage
from boa3_test.test_drive.testrunner.blockchain.storagecollection import StorageCollection
from boa3_test.test_drive.testrunner.blockchain.transaction import TestRunnerTransaction as Transaction
from boa3_test.test_drive.testrunner.blockchain.transactionlog import TestRunnerTransactionLog as TransactionLog


class NeoTestRunner:
    _FOLDER_NAME = 'test-runner'
    _ROOT_FOLDER = os.path.abspath(os.path.curdir) + os.path.sep + _FOLDER_NAME
    _INVOKE_FILE = f'{_FOLDER_NAME}.neo-invoke.json'
    _BATCH_FILE = f'{_FOLDER_NAME}.batch'
    _CHECKPOINT_FILE = f'{_FOLDER_NAME}.neoxp-checkpoint'

    _DEFAULT_ACCOUNT = None

    def __init__(self, neoxp_path: str, runner_id: str = None):
        self._vm_state: VMState = VMState.NONE
        self._gas_consumed: int = 0
        self._result_stack: list[Any] = []
        self._error_message: str | None = None
        self._last_cli_log: str | None = None
        self._cli_log: str = ''

        self._calling_account: Account | None = None
        self._notifications: list[Notification] = []
        self._logs: list[Log] = []
        self._storages: StorageCollection = StorageCollection()

        self._neoxp_abs_path = os.path.abspath(neoxp_path)
        self._neoxp_config = self._set_up_neoxp_config()

        if isinstance(runner_id, str):
            self._file_name: str = None  # defined in the following line
            self.file_name = self._FOLDER_NAME if not runner_id else runner_id
        else:
            self._file_name = self._FOLDER_NAME

        self._first_execution = True

        self._batch = NeoExpressBatch(self._neoxp_config)
        self._contracts = ContractCollection()
        self._invokes = NeoInvokeCollection()
        self._invokes_to_batch = 0
        self._last_execution_results: list[NeoInvokeResult] = []

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value: str):
        if isinstance(value, str) and not value.isspace():
            self._file_name = value
            self._set_up_generate_file_names(value)

    def _set_up_generate_file_names(self, file_name: str):
        self._INVOKE_FILE = f'{file_name}.neo-invoke.json'
        self._BATCH_FILE = f'{file_name}.batch'
        self._CHECKPOINT_FILE = f'{file_name}.neoxp-checkpoint'

    def _set_up_neoxp_config(self) -> NeoExpressConfig:
        neoxp_config = neoxp_utils.get_config_data(self._neoxp_abs_path)
        self._DEFAULT_ACCOUNT = neoxp_config.default_account
        return neoxp_config

    @property
    def vm_state(self) -> VMState:
        return self._vm_state

    @property
    def gas_consumed(self) -> int:
        return self._gas_consumed

    @property
    def result_stack(self) -> list[Any]:
        return self._result_stack.copy()

    @property
    def error(self) -> str | None:
        return self._error_message

    @property
    def cli_log(self) -> str:
        return self._cli_log

    @property
    def notifications(self) -> list[Notification]:
        return self._notifications.copy()

    def get_events(self, event_name: str = None, origin: TestContract = None) -> list[Notification]:
        return self._filter_events(self._notifications, event_name, origin)

    def get_logs(self, origin: TestContract = None) -> list[Log]:
        return self._filter_events(self._logs, origin=origin)

    def _filter_events(self, events: list, event_name: str = None, origin: TestContract = None) -> list:
        if origin is None and event_name is None:
            return events.copy()
        elif origin is None:
            return [n for n in events if n.name == event_name]
        else:
            if hasattr(origin, 'script_hash'):
                origin_bytes = origin.script_hash
            elif hasattr(origin, 'to_array'):
                origin_bytes = origin.to_array()
            else:
                origin_bytes = bytes(origin)

            if event_name is None:
                return [n for n in events if n.origin == origin_bytes]
            else:
                return [n for n in events if (n.name == event_name
                                              and n.origin == origin_bytes)]

    @property
    def logs(self) -> list[Log]:
        return self._logs.copy()

    @property
    def contracts(self) -> ContractCollection:
        return self._contracts

    @property
    def storages(self) -> StorageCollection:
        return self._storages

    @property
    def _root(self) -> str:
        return self._ROOT_FOLDER

    @_root.setter
    def _root(self, value: str):
        if isinstance(value, str) and os.path.exists(value) and os.path.isdir(value):
            sep = os.path.sep
            root = os.path.abspath(value) + sep + self._FOLDER_NAME
            self._ROOT_FOLDER = root

    def _update_cli_log(self, log_to_append: str):
        if self._last_cli_log is None:
            log_connector = '\n' if len(self._cli_log) > 0 and len(log_to_append) > 0 else ''
            self._cli_log += f'{log_connector}{log_to_append}'
        else:
            self._last_cli_log = self._cli_log
            self._cli_log = log_to_append

    def get_genesis_block(self) -> Block:
        return self.get_block(0)

    def get_latest_block(self) -> Block:
        return self.get_block(None)

    def get_block(self, block_hash_or_index: UInt256 | bytes | int) -> Block | None:
        genesis = self._get_genesis_block()
        if isinstance(genesis, Block) and block_hash_or_index in (genesis.hash, genesis.index):
            # genesis block doesn't change between neo express resets
            return genesis

        block = self._get_block(block_hash_or_index)
        if not isinstance(genesis, Block) and isinstance(block, Block) and block.index == 0:
            self._set_genesis_block(block)  # optimization for consecutive executions
        return block

    def _get_genesis_block(self) -> Block | None:
        return neoxp_utils.get_genesis_block(self._neoxp_config)

    def _get_block(self, block_hash_or_index) -> Block | None:
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return neoxp_utils.get_block(self._neoxp_abs_path, block_hash_or_index,
                                     check_point_file=check_point_path)

    def _set_genesis_block(self, genesis):
        if isinstance(genesis, Block):
            self._neoxp_config._genesis_block = genesis

    def get_transaction(self, tx_hash: UInt256 | bytes) -> Transaction | None:
        if isinstance(tx_hash, bytes):
            tx_hash = UInt256(tx_hash)

        return self._get_tx(tx_hash)

    def _get_tx(self, tx_hash: UInt256):
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return neoxp_utils.get_transaction(self._neoxp_abs_path, tx_hash,
                                           check_point_file=check_point_path)

    def get_transaction_result(self, tx_hash: UInt256 | bytes) -> TransactionLog | None:
        if isinstance(tx_hash, bytes):
            tx_hash = UInt256(tx_hash)

        return self._get_tx_log(tx_hash, contract_collection=self._contracts)

    def _get_tx_log(self, tx_hash: UInt256, contract_collection: ContractCollection):
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return neoxp_utils.get_transaction_log(self._neoxp_abs_path, tx_hash,
                                               check_point_file=check_point_path,
                                               contract_collection=contract_collection)

    def deploy_contract(self, nef_path: str, account: Account = None) -> TestContract:
        if not isinstance(nef_path, str) or not nef_path.endswith('.nef'):
            raise ValueError('Requires a .nef file to deploy a contract')
        elif not os.path.exists(nef_path):
            raise FileNotFoundError(f'Could not find file at: {nef_path}')

        if nef_path not in self._contracts:
            contract = self._batch.deploy_contract(nef_path, account)
            if contract.name in self._contracts:
                raise ValueError('Contract with duplicated name')
            self._contracts.append(contract)
        else:
            contract = self._contracts[nef_path]
        return contract

    def call_contract(self, nef_path: str, method: str, *arguments: Any,
                      expected_result_type: type = None) -> NeoInvokeResult:
        if nef_path not in self._contracts:
            contract = self.deploy_contract(nef_path)
        else:
            contract = self._contracts[nef_path]

        return self._invokes.append_contract_invoke(contract, method, *arguments,
                                                    expected_result_type=expected_result_type)

    def run_contract(self, nef_path: str, method: str, *arguments: Any,
                     account: Account = None, witness_scope: WitnessScope = WitnessScope.CalledByEntry,
                     expected_result_type: type = None) -> NeoBatchInvoke:
        if nef_path not in self._contracts:
            contract = self.deploy_contract(nef_path)
        else:
            contract = self._contracts[nef_path]

        if witness_scope != WitnessScope.CalledByEntry:
            # neo express only supports CalledByEntry and Global as witness scopes
            witness_scope = WitnessScope.Global

        invoke = self._invokes.create_contract_invoke(contract, method, *arguments)
        if isinstance(account, Account):
            invoke._invoker = account
        return self._batch.run_contract(invoke,
                                        witness_scope=witness_scope,
                                        expected_result_type=expected_result_type)

    def get_contract(self, contract_id: str | bytes) -> TestContract:
        return self._contracts[contract_id]

    def update_contracts(self, export_checkpoint: bool = False):
        self._generate_root_folder()
        if export_checkpoint:
            self._create_checkpoint_from_batch()
        else:
            self._update_contracts()

    def _update_contracts(self):
        batch_file_path = self.get_full_path(self._BATCH_FILE)
        if self._first_execution:
            check_point_path = None
            self._first_execution = False
        else:
            check_point_path = self.get_full_path(self._CHECKPOINT_FILE)

        batch_has_deploys = self._batch.has_new_deploys()
        log = self._batch.execute(self._neoxp_abs_path, batch_file_path,
                                  check_point_file=check_point_path,
                                  reset=True
                                  )
        self._update_cli_log(log)

        if batch_has_deploys:
            self._contracts.update_after_deploy()

    def execute(self, account: Account = None, get_storage_from: str | TestContract = None,
                clear_invokes: bool = True, add_invokes_to_batch: bool = False):
        self._generate_files()
        invoke_file_path = self.get_full_path(self._INVOKE_FILE)
        cli_args = ['neo-test-runner', invoke_file_path
                    ]

        checkpoint_file = self.get_full_path(self._CHECKPOINT_FILE)
        if os.path.isfile(checkpoint_file):
            cli_args.extend(['--checkpoint', checkpoint_file])

        if isinstance(account, Account):
            cli_args.extend(['--account', account.get_identifier()])
            cli_args.extend(['--express', self._neoxp_abs_path])
        elif account is not None:
            account = None
        self._calling_account = account

        if isinstance(get_storage_from, TestContract):
            get_storage_from = get_storage_from.get_identifier()
        if isinstance(get_storage_from, str):
            cli_args.extend(['--storages', get_storage_from])
        stdout, stderr = self._run_command_line(cli_args)

        try:
            self.reset_state()
            try:
                result = json.loads(stdout)
            except json.JSONDecodeError:
                result = utils.handle_return_error(stdout)

            self._update_runner(result)
        except BaseException:
            self._error_message = stdout

        if add_invokes_to_batch:
            import shutil
            self._invokes_to_batch += 1
            invoke_file_path_to_batch = self.get_full_path(f'{self._file_name}_{self._invokes_to_batch}.neo-invoke.json')
            shutil.copy(invoke_file_path, invoke_file_path_to_batch)
            self._batch.invoke_file(invoke_file_path_to_batch, account=account)

        if clear_invokes:
            self._invokes.clear(state=self._vm_state)

        if self._error_message is not None:
            return self._error_message
        else:
            return self._last_execution_results

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._last_execution_results = []
        self._notifications.clear()
        self._logs.clear()
        self._storages.clear()
        self._last_cli_log = None
        self._error_message = None

    def reset(self):
        self.reset_state()
        self._first_execution = True

        self._batch.clear()
        self._contracts.clear()
        self._invokes.clear()
        self._invokes_to_batch = 0

    def _update_runner(self, result: dict[str, Any]):
        self.reset_state()
        self._error_message = result['exception'] if 'exception' in result else None

        self._last_cli_log = self._cli_log
        if 'state' in result:
            self._vm_state = vmstate.get_vm_state(result['state'])

        if 'gasconsumed' in result:
            self._gas_consumed = int(float(result['gasconsumed']) * 10 ** constants.GAS_DECIMALS)

        if 'stack' in result:
            result_stack = result['stack']
            if isinstance(result_stack, list):
                new_result_stack = [neo_utils.stack_item_from_json(value) for value in result_stack]
            else:
                new_result_stack = [neo_utils.stack_item_from_json(result_stack)]

            self._last_execution_results = self._invokes.set_results(new_result_stack,
                                                                     calling_account=self._calling_account)
            self._result_stack = new_result_stack

        if 'notifications' in result:
            json_notifications = result['notifications']
            if not isinstance(json_notifications, list):
                json_notifications = [json_notifications]

            notifications = []
            for n in json_notifications:
                new = Notification.from_json(n, contract_collection=self._contracts)
                if new is not None:
                    notifications.append(new)
            self._notifications.extend(notifications)

        if 'logs' in result:
            json_logs = result['logs']
            if not isinstance(json_logs, list):
                json_logs = [json_logs]

            logs = []
            for l in json_logs:
                new = Log.from_json(l)
                if new is not None:
                    logs.append(new)
            self._logs.extend(logs)

        if 'storages' in result:
            json_storages = result['storages']
            if not isinstance(json_storages, list):
                json_storages = [json_storages]

            for s in json_storages:
                new = Storage.from_json(s, self._contracts)
                if new is not None:
                    self._storages.append(new)

    def _generate_root_folder(self):
        if not os.path.exists(self._root):
            os.mkdir(self._root)

    def _generate_files(self):
        self._generate_root_folder()

        methods_to_call = [
            (self._create_checkpoint_from_batch, ()),
            (self._generate_invoke_file, ()),
        ]

        self._internal_generate_files(methods_to_call)

    def _internal_generate_files(self, methods_to_call: list[tuple[Callable, Sequence]]):
        for method, args in methods_to_call:
            method(*args)

    def _create_checkpoint_from_batch(self):
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)

        if not os.path.exists(check_point_path) or self._batch.cur_size() > 0:
            self._batch.create_neo_express_checkpoint(check_point_path,
                                                      overwrite=True)
        # update list of contracts
        self._update_contracts()

    def _generate_invoke_file(self):
        invoke_file_content = self._invokes.to_json()
        param_json = json.dumps(invoke_file_content, separators=(',', ':'))
        with open(self.get_full_path(self._INVOKE_FILE), 'wb+') as json_file:
            json_file.write(String(param_json).to_bytes())

    def get_full_path(self, file_name: str):
        return self._root + os.path.sep + file_name

    def _run_command_line(self, args: list[str]) -> tuple[str, str]:
        process = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        return process.communicate()

    def increase_block(self, block_to_mint: int = None, time_interval_in_secs: int = 0):
        self._batch.mint_block(block_to_mint, time_interval_in_secs)

    def oracle_enable(self, account: Account):
        self._batch.oracle_enable(account)

    def oracle_response(self, url: str, response_path: str, request_id: int = None) -> list[UInt256]:
        # add to command to batch file and get the tx id
        self._batch.oracle_response(url, response_path, request_id=request_id)
        return self._get_oracle_resp(url, response_path, request_id)

    def _get_oracle_resp(self, url: str, response_path: str, request_id: int = None) -> list[UInt256]:
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)
        return neoxp_utils.oracle_response(self._neoxp_abs_path, url, response_path, request_id,
                                           check_point_file=check_point_path)
