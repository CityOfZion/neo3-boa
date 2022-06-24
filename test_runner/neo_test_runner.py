import json
import os.path
import subprocess
from typing import Any, Dict, List, Optional, Tuple, Union

from boa3 import constants
from boa3.neo import utils as neo_utils
from boa3.neo.smart_contract.VoidType import VoidType
from boa3.neo.vm.type.String import String
from boa3.neo3.core.types import UInt160
from boa3.neo3.vm import VMState, vmstate
from test_runner import neoxp_utils
from test_runner.blockchain import *
from test_runner.blockchain.contractcollection import ContractCollection
from test_runner.blockchain.storagecollection import StorageCollection
from test_runner.neoxp.batch import NeoExpressBatch
from test_runner.neoxp.neoinvoke import NeoInvoke


class NeoTestRunner:
    _FOLDER_NAME = 'test-runner'
    _ROOT_FOLDER = os.path.abspath(os.path.curdir) + os.path.sep + _FOLDER_NAME
    _INVOKE_FILE = f'{_FOLDER_NAME}.neo-invoke.json'
    _BATCH_FILE = f'{_FOLDER_NAME}.batch'
    _CHECKPOINT_FILE = f'{_FOLDER_NAME}.neoxp-checkpoint'
    _NEO_EXPRESS_FILE = f'{_FOLDER_NAME}.neo-express'

    def __init__(self, root_test_folder: str = None):
        self._root = root_test_folder

        self._vm_state: VMState = VMState.NONE
        self._gas_consumed: int = 0
        self._result_stack: List[Any] = []
        self._error_message: Optional[str] = None

        self._notifications: List[Notification] = []
        self._logs: List[Log] = []
        self._contracts: ContractCollection = ContractCollection()
        self._storages: StorageCollection = StorageCollection()

        self._batch = NeoExpressBatch()
        self._init_neo_express()

    @property
    def error(self) -> Optional[str]:
        return self._error_message

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

    def silent_run(self, contract_id: Union[str, bytes], method: str, *arguments: Any):
        contract_hash = self._get_contract_hash_or_name(contract_id)
        invoke = self._get_invoke(contract_hash, method, *arguments)
        self._deploy_contract(contract_id, True)
        self._batch.run_contract(invoke)

    def run(self, contract_id: Union[str, bytes], method: str, *arguments: Any,
            get_storage: bool = False,
            reset_runner: bool = False) -> Any:

        contract_hash = self._get_contract_hash_or_name(contract_id)
        invoke = self._get_invoke(contract_hash, method, *arguments)

        self._batch.mint_block(1)
        self._generate_files(contract_id, invoke)
        self._batch.pop()  # remove the forced block minting from batch for optimization

        cli_args = ['neo-test-runner', self._INVOKE_FILE,
                    '--checkpoint', self._CHECKPOINT_FILE,
                    '--express', self._NEO_EXPRESS_FILE
                    ]

        if get_storage and contract_id in self._contracts:
            calling_contract = self._contracts[contract_id]
            if hasattr(calling_contract, 'name'):
                cli_args.extend(['--storages', calling_contract.name])
        stdout, stderr = self._run_command_line(cli_args)

        if reset_runner:
            self.reset_runner()
        else:
            self.reset_state()

        try:
            result = json.loads(stdout)

            self._update_runner(result)
            if self._error_message is None:
                self._batch.run_contract(invoke)
        except BaseException:
            self._error_message = stdout

        if self._error_message is not None:
            return self._error_message
        else:
            # TODO: convert the result to the return type of the function in the manifest
            return self._result_stack[-1] if len(self._result_stack) > 0 else VoidType

    @property
    def _root(self) -> str:
        return self._ROOT_FOLDER

    @_root.setter
    def _root(self, value: str):
        if isinstance(value, str) and os.path.exists(value) and os.path.isdir(value):
            sep = os.path.sep
            root = os.path.abspath(value) + sep + self._FOLDER_NAME
            self._ROOT_FOLDER = root
            self._INVOKE_FILE = root + sep + NeoTestRunner._INVOKE_FILE
            self._BATCH_FILE = root + sep + NeoTestRunner._BATCH_FILE
            self._CHECKPOINT_FILE = root + sep + NeoTestRunner._CHECKPOINT_FILE
            self._NEO_EXPRESS_FILE = root + sep + NeoTestRunner._NEO_EXPRESS_FILE

        elif not self._INVOKE_FILE.startswith(self._ROOT_FOLDER):
            root_folder = self._ROOT_FOLDER + os.path.sep
            self._INVOKE_FILE = root_folder + NeoTestRunner._INVOKE_FILE
            self._BATCH_FILE = root_folder + NeoTestRunner._BATCH_FILE
            self._CHECKPOINT_FILE = root_folder + NeoTestRunner._CHECKPOINT_FILE
            self._NEO_EXPRESS_FILE = root_folder + NeoTestRunner._NEO_EXPRESS_FILE

    def _get_contract_hash_or_name(self, contract_id: Union[str, bytes]) -> Union[str, UInt160]:
        if isinstance(contract_id, str):
            if contract_id in self._contracts:
                contract = self._contracts[contract_id]
                return contract.name if hasattr(contract, 'name') else contract.script_hash

            try:
                return UInt160.from_string(contract_id)
            except BaseException as e:
                if not contract_id.endswith('.nef'):
                    raise e
                manifest_file = contract_id.replace('.nef', '.manifest.json')
                if os.path.exists(manifest_file):
                    with open(manifest_file) as manifest_output:
                        import json
                        manifest = json.loads(manifest_output.read())
                        return manifest['name']

                raise e
        else:
            return UInt160(contract_id)

    def _generate_root_folder(self):
        if not os.path.exists(self._root):
            os.mkdir(self._root)

    def _generate_files(self, contract_id: Union[str, bytes], invoke: NeoInvoke):
        self._generate_root_folder()

        self._generate_checkpoint(contract_id)
        self._generate_batch_file()
        self._batch.pop()  # remove checkpoint operation from batch after generating the file
        if os.path.exists(contract_id) and contract_id.endswith('.nef') and contract_id not in self.contracts:
            contract = neoxp_utils.get_last_deployed_contract(self._NEO_EXPRESS_FILE)
            contract.path = contract_id
            self._contracts.append(contract)

        self._generate_invoke_file(invoke)

    def _init_neo_express(self):
        self._generate_root_folder()
        if not os.path.exists(self._NEO_EXPRESS_FILE):
            neoxp_utils.create_neo_express_instance(self._NEO_EXPRESS_FILE)
        else:
            neoxp_utils.reset_neo_express_instance(self._NEO_EXPRESS_FILE)

    def _deploy_contract(self, contract_id: str, deploy_and_execute: bool = False):
        if os.path.exists(contract_id) and contract_id.endswith('.nef') and contract_id not in self.contracts:
            self._batch.deploy_contract(contract_id)
            if deploy_and_execute:
                self._generate_batch_file()
                contract = neoxp_utils.get_last_deployed_contract(self._NEO_EXPRESS_FILE)
                contract.path = contract_id
                self._contracts.append(contract)

    def _generate_checkpoint(self, contract_id: Union[str, UInt160]):
        if os.path.exists(contract_id) and contract_id.endswith('.nef'):
            self._deploy_contract(contract_id)
            self._batch.create_neo_express_checkpoint(self._CHECKPOINT_FILE, True)

    def _generate_batch_file(self):
        assert self._batch.write(self._BATCH_FILE)
        neoxp_utils.run_batch(self._NEO_EXPRESS_FILE, self._BATCH_FILE)

    def _generate_invoke_file(self, invoke: NeoInvoke):
        test_engine_args = invoke.to_json()
        param_json = json.dumps(test_engine_args, separators=(',', ':'))
        with open(self._INVOKE_FILE, 'wb+') as json_file:
            json_file.write(String(param_json).to_bytes())

    def _get_invoke(self, contract_hash: UInt160, method: str, *args: Any) -> NeoInvoke:
        return NeoInvoke(contract_hash, method, *args)

    def _update_runner(self, result: Dict[str, Any]):
        self._error_message = result['exception'] if 'exception' in result else None

        if 'state' in result:
            self._vm_state = vmstate.get_vm_state(result['state'])

        if 'gasconsumed' in result:
            self._gas_consumed = int(float(result['gasconsumed']) * 10 ** constants.GAS_DECIMALS)

        if 'stack' in result:
            result_stack = result['stack']
            if isinstance(result_stack, list):
                self._result_stack = [neo_utils.stack_item_from_json(value) for value in result_stack]
            else:
                self._result_stack = [neo_utils.stack_item_from_json(result_stack)]

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

            storages = []
            for s in json_storages:
                new = Storage.from_json(s, self._contracts)
                if new is not None:
                    storages.append(new)
            self._storages = storages

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._error_message = None

    def reset_runner(self):
        self.reset_state()
        self._notifications.clear()
        self._logs.clear()
        self._contracts.clear()
        self._storages.clear()
        self._batch.clear()
        neoxp_utils.reset_neo_express_instance(self._NEO_EXPRESS_FILE)

    def _run_command_line(self, args: List[str]) -> Tuple[str, str]:
        process = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
        return process.communicate()
