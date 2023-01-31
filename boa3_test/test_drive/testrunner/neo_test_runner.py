import json
import os.path
import subprocess
from typing import Any, List, Tuple, Dict, Optional, Union, Type

from boa3.internal import env, constants
from boa3.internal.neo import utils as neo_utils
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import vmstate, VMState
from boa3_test.test_drive.model.invoker.neoinvokecollection import NeoInvokeCollection
from boa3_test.test_drive.model.invoker.neoinvokeresult import NeoInvokeResult
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.model.wallet.account import Account
from boa3_test.test_drive.neoxp import utils as neoxp_utils
from boa3_test.test_drive.neoxp.batch import NeoExpressBatch
from boa3_test.test_drive.testrunner.blockchain.log import TestRunnerLog as Log
from boa3_test.test_drive.testrunner.blockchain.notification import TestRunnerNotification as Notification
from boa3_test.test_drive.testrunner.blockchain.storage import TestRunnerStorage as Storage
from boa3_test.test_drive.testrunner.blockchain.storagecollection import StorageCollection


class NeoTestRunner:
    _FOLDER_NAME = 'test-runner'
    _ROOT_FOLDER = os.path.abspath(os.path.curdir) + os.path.sep + _FOLDER_NAME
    _INVOKE_FILE = f'{_FOLDER_NAME}.neo-invoke.json'
    _BATCH_FILE = f'{_FOLDER_NAME}.batch'
    _CHECKPOINT_FILE = f'{_FOLDER_NAME}.neoxp-checkpoint'

    _DEFAULT_ACCOUNT = neoxp_utils.get_account_by_name('genesis')

    def __init__(self, neoxp_path: str = None):
        self._vm_state: VMState = VMState.NONE
        self._gas_consumed: int = 0
        self._result_stack: List[Any] = []
        self._error_message: Optional[str] = None
        self._last_cli_log: Optional[str] = None
        self._cli_log: str = ''

        self._calling_account: Optional[Account] = None
        self._notifications: List[Notification] = []
        self._logs: List[Log] = []
        self._storages: StorageCollection = StorageCollection()

        if not isinstance(neoxp_path, str):
            neoxp_path = f'{env.NEO_EXPRESS_INSTANCE_DIRECTORY}{os.path.sep}default.neo-express'
        self._neoxp_abs_path = os.path.abspath(neoxp_path)

        self._batch = NeoExpressBatch()
        self._batch_size_since_last_update = -1
        self._batch_size_since_last_checkpoint = 0
        self._contracts = ContractCollection()
        self._invokes = NeoInvokeCollection()
        self._last_execution_results: List[NeoInvokeResult] = []

    @property
    def vm_state(self) -> VMState:
        return self._vm_state

    @property
    def gas_consumed(self) -> int:
        return self._gas_consumed

    @property
    def result_stack(self) -> List[Any]:
        return self._result_stack.copy()

    @property
    def error(self) -> Optional[str]:
        return self._error_message

    @property
    def cli_log(self) -> str:
        return self._cli_log

    @property
    def notifications(self) -> List[Notification]:
        return self._notifications.copy()

    @property
    def logs(self) -> List[Log]:
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

    def add_neo(self, script_hash_or_address: Union[bytes, str], amount: int):
        address = neoxp_utils.get_account_identifier_from_script_hash_or_name(script_hash_or_address)
        self._batch.transfer_assets(sender=self._DEFAULT_ACCOUNT.name, receiver=address,
                                    quantity=amount, asset='NEO')

    def add_gas(self, script_hash_or_address: Union[bytes, str], amount: int):
        address = neoxp_utils.get_account_identifier_from_script_hash_or_name(script_hash_or_address)
        self._batch.transfer_assets(sender=self._DEFAULT_ACCOUNT.name, receiver=address,
                                    quantity=amount, asset='GAS')

    def deploy_contract(self, nef_path: str, account: Account = None) -> TestContract:
        if not isinstance(nef_path, str) or not nef_path.endswith('.nef'):
            raise ValueError('Requires a .nef file to deploy a contract')

        if nef_path not in self._contracts:
            contract = self._batch.deploy_contract(nef_path, account)
            if contract.name in self._contracts:
                raise ValueError('Contract with duplicated name')
            self._contracts.append(contract)
        else:
            contract = self._contracts[nef_path]
        return contract

    def call_contract(self, nef_path: str, method: str, *arguments: Any,
                      expected_result_type: Type = None) -> NeoInvokeResult:
        if nef_path not in self._contracts:
            contract = self.deploy_contract(nef_path)
        else:
            contract = self._contracts[nef_path]

        return self._invokes.append_contract_invoke(contract, method, *arguments,
                                                    expected_result_type=expected_result_type)

    def get_contract(self, contract_id: Union[str, bytes]) -> TestContract:
        return self._contracts[contract_id]

    def update_contracts(self):
        cur_batch_size = self._batch.cur_size()
        batch_file_path = self.get_full_path(self._BATCH_FILE)

        if self._batch_size_since_last_update < cur_batch_size:
            log = self._batch.execute(self._neoxp_abs_path, batch_file_path, reset=True)
            self._update_cli_log(log)

            if self._batch.has_new_deploys_since(self._batch_size_since_last_update):
                deployed_contracts = neoxp_utils.get_deployed_contracts(self._neoxp_abs_path)
                self._contracts.replace(deployed_contracts)
            self._batch_size_since_last_update = cur_batch_size

    def execute(self, account: Account = None, get_storage_from: Union[str, TestContract] = None):
        self._generate_files()
        cli_args = ['neo-test-runner', self.get_full_path(self._INVOKE_FILE)
                    ]

        if self._batch_size_since_last_checkpoint > 0:
            cli_args.extend(['--checkpoint', self.get_full_path(self._CHECKPOINT_FILE)])

        if isinstance(account, Account):
            cli_args.extend(['--account', account.get_identifier()])
        elif account is not None:
            account = None
        self._calling_account = account

        if isinstance(get_storage_from, TestContract):
            get_storage_from = get_storage_from.get_identifier()
        if isinstance(get_storage_from, str):
            cli_args.extend(['--storages', get_storage_from])
        stdout, stderr = self._run_command_line(cli_args)

        try:
            result = json.loads(stdout)
            self._update_runner(result)
            self._invokes.clear()
        except BaseException:
            self._error_message = stdout

        if self._error_message is not None:
            return self._error_message
        else:
            return self._last_execution_results

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._last_execution_results = []
        self._storages.clear()
        self._last_cli_log = None
        self._error_message = None

    def reset(self):
        self.reset_state()
        self._notifications.clear()
        self._logs.clear()

        self._batch.clear()
        self._batch_size_since_last_update = -1
        self._batch_size_since_last_checkpoint = 0
        self._contracts.clear()
        self._invokes.clear()

    def _update_runner(self, result: Dict[str, Any]):
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
                new = Notification.from_json(n)
                if new is not None:
                    notifications.append(new)
            self._notifications = notifications

        if 'logs' in result:
            json_logs = result['logs']
            if not isinstance(json_logs, list):
                json_logs = [json_logs]

            logs = []
            for l in json_logs:
                new = Log.from_json(l)
                if new is not None:
                    logs.append(new)
            self._logs = logs

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
        self._create_checkpoint_from_batch()
        self._generate_invoke_file()

    def _create_checkpoint_from_batch(self):
        check_point_path = self.get_full_path(self._CHECKPOINT_FILE)

        if self._batch_size_since_last_checkpoint < self._batch.cur_size():
            self._batch.create_neo_express_checkpoint(check_point_path,
                                                      overwrite=True)
            self._batch_size_since_last_checkpoint = self._batch.cur_size()
        # update list of contracts
        self.update_contracts()

    def _generate_invoke_file(self):
        invoke_file_content = self._invokes.to_json()
        param_json = json.dumps(invoke_file_content, separators=(',', ':'))
        with open(self.get_full_path(self._INVOKE_FILE), 'wb+') as json_file:
            json_file.write(String(param_json).to_bytes())

    def get_full_path(self, file_name: str):
        return self._root + os.path.sep + file_name

    def _run_command_line(self, args: List[str]) -> Tuple[str, str]:
        process = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        return process.communicate()

    def increase_block(self, new_height: int = None):
        self._batch.mint_block(new_height)
