import threading
from os import path
from typing import Any, Dict, List, Optional, Tuple, Union

from boa3.internal import constants
from boa3.internal.neo.smart_contract.VoidType import VoidType
from boa3.internal.neo.smart_contract.notification import Notification
from boa3.internal.neo.utils import contract_parameter_to_json, stack_item_from_json
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.core.types import UInt160
from boa3.internal.neo3.vm import VMState, vmstate
from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope
from boa3_test.tests.test_classes.block import Block
from boa3_test.tests.test_classes.contractcollection import ContractCollection
from boa3_test.tests.test_classes.signer import Signer
from boa3_test.tests.test_classes.storage import Storage
from boa3_test.tests.test_classes.testcontract import TestContract
from boa3_test.tests.test_classes.transaction import Transaction
from boa3_test.tests.test_classes.transactionattribute import oracleresponse

_TEST_ENGINE_LOCK = threading.Lock()  # avoid race condition when calling test engine


class TestEngine:
    def __init__(self, root_path: Optional[str] = None):
        if root_path is None:
            from boa3.internal import env
            root_path = env.TEST_ENGINE_DIRECTORY

        engine_path = '{0}/Neo.TestEngine.dll'.format(root_path)
        if not path.exists(engine_path):
            raise FileNotFoundError(
                "File at {0} was not found.\n"
                "Visit the docs or the README file and search for 'TestEngine' to correctly install it."
                .format(engine_path))

        self.use_contract_custom_name = False

        self._test_engine_path = engine_path
        self._vm_state: VMState = VMState.NONE
        self._executed_script_hash: Optional[UInt160] = None
        self._calling_script_hash: Optional[UInt160] = None
        self._gas_consumed: int = 0
        self._result_stack: List[Any] = []

        self._storage: Storage = Storage()
        self._notifications: List[Notification] = []
        self._height: int = 0
        self._blocks: List[Block] = []

        self._current_tx: Optional[Transaction] = None
        self._accounts: List[Signer] = []
        self._contract_paths: ContractCollection = ContractCollection()

        self._error_message: Optional[str] = None
        self._neo_balance_prefix: bytes = b'\x14'

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
    def executed_script_hash(self) -> Optional[UInt160]:
        return self._executed_script_hash

    @property
    def calling_script_hash(self) -> Optional[UInt160]:
        return self._calling_script_hash

    @property
    def result_stack(self) -> List[Any]:
        return self._result_stack.copy()

    @property
    def notifications(self) -> List[Notification]:
        return self._notifications.copy()

    def get_events(self, event_name: str = None, origin: Union[UInt160, bytes] = None) -> List[Notification]:
        if origin is None:
            return [n for n in self._notifications if n.name == event_name or event_name is None]
        else:
            origin_bytes = origin.to_array() if isinstance(origin, UInt160) else bytes(origin)
            return [n for n in self._notifications if ((n.name == event_name or event_name is None)
                                                       and n.origin == origin_bytes)]

    def _get_contract_nef(self, contract_path: str) -> str:
        if contract_path.endswith('.py'):
            if self.use_contract_custom_name:
                from boa3_test.test_drive import utils
                name_without_extension, _ = contract_path.split('.py', maxsplit=1)
                contract_path = f'{utils.create_custom_id(name_without_extension, use_time=False)}.py'

            contract_path = contract_path.replace('.py', '.nef')
        return contract_path

    @property
    def storage(self) -> Storage:
        return self._storage.copy()

    def storage_get(self, key: Union[str, bytes], contract_path: str) -> Any:
        if isinstance(key, str):
            key = String(key).to_bytes()

        if contract_path.endswith('.py'):
            contract_path = self._get_contract_nef(contract_path)
        if contract_path not in self.contracts:
            return None

        contract_id = self._get_contract_id(contract_path)
        storage_key = Storage.build_key(key, contract_id)
        if storage_key in self._storage:
            return self._storage[storage_key]
        else:
            return None

    def storage_put(self, key: Union[str, bytes], value: Any, contract_path: str):
        if isinstance(key, str):
            key = String(key).to_bytes()

        if contract_path.endswith('.py'):
            contract_path = self._get_contract_nef(contract_path)
        if contract_path in self.contracts:
            contract_id = self._get_contract_id(contract_path)
            storage_key = Storage.build_key(key, contract_id)

            self._storage[storage_key] = value

    def set_storage(self, storage: Dict[Tuple[Union[str, bytes], str], Any]):
        self._storage.clear(delete_deploy_data=False)
        for (key, contract_path), value in storage.items():
            self.storage_put(key, value, contract_path)

    def storage_delete(self, key: Union[str, bytes], contract_path: str):
        if isinstance(key, str):
            key = String(key).to_bytes()

        if contract_path.endswith('.py'):
            contract_path = self._get_contract_nef(contract_path)
        if contract_path not in self.contracts:
            return None

        contract_id = self._get_contract_id(contract_path)
        storage_key = Storage.build_key(key, contract_id)

        if storage_key in self._storage:
            self._storage.pop(key)

    def add_neo(self, script_hash: bytes, amount: int) -> bool:
        return self._storage.add_token(constants.NEO_SCRIPT, script_hash, amount)

    def add_gas(self, script_hash: bytes, amount: int) -> bool:
        return self._storage.add_token(constants.GAS_SCRIPT, script_hash, amount)

    def set_calling_script_hash(self, calling_hash: bytes) -> bool:
        if len(calling_hash) != constants.SIZE_OF_INT160:
            return False

        calling_script_hash = UInt160(calling_hash)
        account = Signer(calling_script_hash, WitnessScope.CalledByEntry)
        if account in self._accounts:
            account_index = self._accounts.index(account)
            if account_index != 0:  # the calling hash should be the first signer
                account = self._accounts.pop(account_index)
                account.add_scope(WitnessScope.CalledByEntry)

        self._accounts.insert(0, account)
        self._calling_script_hash = calling_script_hash

    def add_signer_account(self, account_address: bytes, account_scope: WitnessScope = WitnessScope.CalledByEntry,
                           permissions: list = None):
        account = Signer(UInt160(account_address), account_scope)
        if permissions is None:
            permissions = []

        account.set_permissions(permissions)
        if account not in self._accounts:
            self._accounts.append(account)

    @property
    def contracts(self) -> List[str]:
        return [contract.path for contract in self._contract_paths]

    def add_contract(self, contract_nef_path: str):
        if contract_nef_path.endswith('.nef') and contract_nef_path not in self._contract_paths:
            manifest_path = contract_nef_path.replace('.nef', '.manifest.json')
            if not path.exists(manifest_path):
                raise FileNotFoundError(manifest_path)
            self._contract_paths.append(TestContract(contract_nef_path, manifest_path))

    def remove_contract(self, contract_index_or_path: Union[int, str]):
        if isinstance(contract_index_or_path, str):
            contracts = self.contracts
            if contract_index_or_path in contracts:
                index = contracts.index(contract_index_or_path)
            else:
                index = -1
        else:
            index = contract_index_or_path

        if 0 <= index < len(self._contract_paths):
            return self._contract_paths.pop(index)

    def _get_contract_id(self, contract_path: str) -> int:
        contracts = self.contracts
        if path.isfile(contract_path) and contract_path not in contracts:
            with open(contract_path, mode='rb') as nef:
                from boa3.internal.neo.contracts.neffile import NefFile
                script_hash = NefFile.deserialize(nef.read()).script_hash

            return self._storage.get_contract_id(script_hash)

        if contract_path in contracts:
            return contracts.index(contract_path) + 1
        return -1

    @property
    def height(self) -> int:
        return self.current_block.index if self.current_block is not None else self._height

    @property
    def blocks(self) -> List[Block]:
        return sorted(self._blocks, key=lambda block: block.index)

    @property
    def current_block(self) -> Optional[Block]:
        return self.blocks[-1] if len(self._blocks) > 0 else None

    def increase_block(self, new_height: int = None) -> Block:
        if self.current_block is None:
            if new_height is None or new_height <= self._height:
                new_height = self._height
        else:
            if new_height is None or new_height <= self._height:
                new_height = self.height + 1
            self._height = new_height

        if new_height < 1:
            # don't use height 0 because this is the genesis block index
            new_height = 1
        new_block = Block(new_height)
        self.add_block(new_block)
        return new_block

    def add_block(self, block: Block) -> bool:
        success = len(list(filter(lambda b: b.index == block.index, self._blocks))) == 0
        if success:
            self._blocks.append(block)
        return success

    def get_transactions(self) -> List[Transaction]:
        txs = []
        for block in self._blocks:
            txs.extend(block.get_transactions())
        return txs

    def add_transaction(self, *transaction: Transaction):
        if self.current_block is None:
            self.increase_block()

        current_block = self.current_block
        for tx in transaction:
            current_block.add_transaction(tx)

    def run_oracle_response(self, request_id: int, oracle_response: oracleresponse.OracleResponseCode,
                            result: bytes, reset_engine: bool = False,
                            rollback_on_fault: bool = True) -> Any:
        request_ids = [x.arguments[0] if isinstance(x.arguments, (tuple, list)) and len(x.arguments) > 0
                       else x.arguments
                       for x in self.get_events('OracleRequest', constants.ORACLE_SCRIPT)]

        assert request_id in request_ids, 'Request ID not found'
        self._current_tx = Transaction(b'')
        self._current_tx.add_attribute(oracleresponse.OracleResponse(request_id, oracle_response, result))

        return self.run(UInt160(constants.ORACLE_SCRIPT), 'finish',
                        reset_engine=reset_engine,
                        rollback_on_fault=rollback_on_fault)

    def run(self, contract_id: Union[str, UInt160], method: str, *arguments: Any, reset_engine: bool = False,
            rollback_on_fault: bool = True) -> Any:
        import json
        import subprocess

        if isinstance(contract_id, str) and contract_id not in self.contracts:
            self.add_contract(contract_id)

        # build an UInt160 value if the contract_id is not a path
        if isinstance(contract_id, bytes) and not isinstance(contract_id, UInt160):
            contract_id = UInt160(contract_id)

        test_engine_args = self.to_json(contract_id, method, *arguments)
        param_json = json.dumps(test_engine_args, separators=(',', ':'))

        with _TEST_ENGINE_LOCK:
            try:
                process = subprocess.Popen(['dotnet', self._test_engine_path, param_json],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           text=True)
            except BaseException:
                json_path = '{0}/test-engine-test.json'.format(path.curdir)
                with open(json_path, 'wb+') as json_file:
                    json_file.write(String(param_json).to_bytes())
                    json_file.close()

                process = subprocess.Popen(['dotnet', self._test_engine_path, json_path],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT,
                                           text=True)

            stdout, stderr = process.communicate()

        if reset_engine:
            self.reset_engine()
        else:
            self.reset_state()

        stdout = stdout.splitlines()[-1]

        try:
            result = json.loads(stdout)

            self._error_message = result['error'] if 'error' in result else None

            if 'vmstate' in result:
                self._vm_state = vmstate.get_vm_state(result['vmstate'])

            if 'executedscripthash' in result:
                try:
                    self._executed_script_hash = UInt160.from_string(result['executedscripthash'])
                except BaseException:
                    self._executed_script_hash = None

            if 'callingscripthash' in result:
                try:
                    calling_script_hash = UInt160.from_string(result['callingscripthash'])
                except BaseException:
                    calling_script_hash = None
                self._calling_script_hash = calling_script_hash

            if 'gasconsumed' in result:
                self._gas_consumed = int(result['gasconsumed'])

            if 'resultstack' in result:
                if isinstance(result['resultstack'], list):
                    self._result_stack = [stack_item_from_json(value) for value in result['resultstack']]
                else:
                    self._result_stack = [stack_item_from_json(result['resultstack'])]

            if self._vm_state is VMState.HALT or not rollback_on_fault:
                if 'notifications' in result:
                    json_storage = result['notifications']
                    if not isinstance(json_storage, list):
                        json_storage = [json_storage]

                    notifications = []
                    for n in json_storage:
                        new = Notification.from_json(n)
                        if new is not None:
                            notifications.append(new)
                    self._notifications.extend(notifications)

                if 'storage' in result:
                    json_storage = result['storage']
                    self._storage = Storage.from_json(json_storage)

                    for contract in self._contract_paths.copy():
                        if (not isinstance(contract, TestContract)
                                or contract.script_hash is None
                                or not self._storage.has_contract(contract.script_hash)):
                            self.remove_contract(contract.path)

                if 'currentblock' in result:
                    current_block = Block.from_json(result['currentblock'])

                    existing_block = next((block for block in self._blocks if block.index == current_block.index), None)
                    if existing_block is not None:
                        self._blocks.remove(existing_block)
                    self._blocks.append(current_block)

                if 'transaction' in result and self._vm_state is VMState.HALT:
                    block = self.current_block
                    if block is None:
                        block = self.increase_block(self.height)

                    tx = Transaction.from_json(result['transaction'])
                    block.add_transaction(tx)

        except BaseException as e:
            self._error_message = str(e)

        if len(self._result_stack) > 0:
            return self._filter_result(self._result_stack[0], method, contract_id)
        return VoidType

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._executed_script_hash = None
        self._calling_script_hash = None
        self._gas_consumed = 0
        self._result_stack = []
        self._accounts = []
        self._current_tx = None
        self._error_message = None

    def reset_engine(self):
        self.reset_state()
        self._notifications.clear()
        self._storage.clear()
        self._contract_paths.clear()

    def _filter_result(self, value: Any, called_method: str, contract_id=None):
        if contract_id is None:
            contract_id = self._executed_script_hash

        called_contract = self._contract_paths[contract_id]
        if not isinstance(called_contract, TestContract):
            return value

        converted_value = value
        expected_return_type = called_contract.get_method_return_type(called_method)

        if expected_return_type is StackItemType.Boolean:
            converted_value = bool(value)
        elif expected_return_type is StackItemType.Integer:
            if isinstance(value, str):
                converted_value = String(value).to_bytes(min_length=1)

            if isinstance(converted_value, bytes):
                converted_value = Integer.from_bytes(value)
            else:
                try:
                    converted_value = int(value)
                except BaseException:
                    converted_value = value
        elif expected_return_type is StackItemType.ByteString:
            if isinstance(value, int):
                converted_value = Integer(value).to_byte_array(min_length=1)

        return converted_value

    def to_json(self, contract_id: Union[str, UInt160], method: str, *args: Any) -> Dict[str, Any]:
        json = {
            'path': contract_id if isinstance(contract_id, str) else '',
            'scripthash': str(contract_id) if not isinstance(contract_id, str) else None,
            'method': method,
            'arguments': [contract_parameter_to_json(x) for x in args],
            'storage': self._storage.to_json(),
            'contracts': [{'nef': contract_path} for contract_path in self.contracts],
            'signeraccounts': [address.to_json() for address in self._accounts],
            'callingscripthash': (self._calling_script_hash if self._calling_script_hash is None
                                  else str(self._calling_script_hash)),
            'height': self.height,
            'blocks': [block.to_json() for block in self.blocks]
        }
        if isinstance(self._current_tx, Transaction):
            json['currenttx'] = self._current_tx.to_json()
        return json
