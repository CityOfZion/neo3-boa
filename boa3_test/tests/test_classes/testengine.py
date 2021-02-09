from os import path
from typing import Any, Dict, List, Optional, Union

from boa3 import constants
from boa3.neo import to_hex_str
from boa3.neo.smart_contract.VoidType import VoidType
from boa3.neo.smart_contract.notification import Notification
from boa3.neo.utils import contract_parameter_to_json, stack_item_from_json
from boa3.neo.vm.type.String import String
from boa3.neo3.core.types import UInt160
from boa3.neo3.vm import VMState
from boa3_test.tests.test_classes.block import Block
from boa3_test.tests.test_classes.storage import Storage
from boa3_test.tests.test_classes.transaction import Transaction


class TestEngine:
    def __init__(self, root_path: Optional[str] = None):
        if root_path is None:
            import env
            root_path = env.TEST_ENGINE_DIRECTORY

        engine_path = '{0}/Neo.TestEngine.dll'.format(root_path)
        if not path.exists(engine_path):
            raise FileNotFoundError(
                "File at {0} was not found.\n"
                "Visit the docs or the README file and search for 'TestEngine' to correctly install it."
                .format(engine_path))

        self._test_engine_path = engine_path
        self._vm_state: VMState = VMState.NONE
        self._gas_consumed: int = 0
        self._result_stack: List[Any] = []

        self._storage: Storage = Storage()
        self._notifications: List[Notification] = []
        self._height: int = 0
        self._blocks: List[Block] = []

        self._accounts: List[bytes] = []
        self._contract_paths: List[str] = []

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
    def result_stack(self) -> List[Any]:
        return self._result_stack.copy()

    @property
    def notifications(self) -> List[Notification]:
        return self._notifications.copy()

    def get_events(self, event_name: str) -> List[Notification]:
        return [n for n in self._notifications if n.name == event_name]

    @property
    def storage(self) -> Storage:
        return self._storage.copy()

    def storage_get(self, key: Union[str, bytes]) -> Any:
        if isinstance(key, str):
            key = String(key).to_bytes()

        if key in self._storage:
            return self._storage[key]
        else:
            return None

    def storage_put(self, key: Union[str, bytes], value: Any):
        if isinstance(key, str):
            key = String(key).to_bytes()

        self._storage[key] = value

    def set_storage(self, storage: Dict[Union[str, bytes], Any]):
        self._storage.clear()
        for key, value in storage.items():
            self.storage_put(key, value)

    def storage_delete(self, key: Union[str, bytes]):
        if isinstance(key, str):
            key = String(key).to_bytes()

        if key in self._storage:
            self._storage.pop(key)

    def add_neo(self, script_hash: bytes, amount: int) -> bool:
        return self._storage.add_token(constants.NEO_SCRIPT, script_hash, amount)

    def add_gas(self, script_hash: bytes, amount: int) -> bool:
        return self._storage.add_token(constants.GAS_SCRIPT, script_hash, amount)

    def add_signer_account(self, account: bytes):
        if account not in self._accounts:
            self._accounts.append(account)

    @property
    def contracts(self) -> List[str]:
        return self._contract_paths.copy()

    def add_contract(self, contract_nef_path: str):
        if contract_nef_path.endswith('.nef') and contract_nef_path not in self._contract_paths:
            self._contract_paths.append(contract_nef_path)

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

    def run(self, nef_path: Union[str, UInt160], method: str, *arguments: Any, reset_engine: bool = False,
            rollback_on_fault: bool = True) -> Any:
        import json
        import subprocess

        test_engine_args = self.to_json(nef_path, method, *arguments)
        param_json = json.dumps(test_engine_args, separators=(',', ':'))
        process = subprocess.Popen(['dotnet', self._test_engine_path, param_json],
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
            if 'vm_state' in result:
                self._vm_state = VMState.get_vm_state(result['vm_state'])

            if 'gasconsumed' in result:
                self._gas_consumed = result['gasconsumed']

            if 'result_stack' in result:
                if isinstance(result['result_stack'], list):
                    self._result_stack = [stack_item_from_json(value) for value in result['result_stack']]
                else:
                    self._result_stack = [stack_item_from_json(result['result_stack'])]

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
                    self._notifications = notifications

                if 'storage' in result:
                    json_storage = result['storage']
                    self._storage = Storage.from_json(json_storage)

                if 'blocks' in result:
                    blocks_json = result['blocks']
                    if not isinstance(blocks_json, list):
                        blocks_json = [blocks_json]

                    self._blocks = sorted([Block.from_json(js) for js in blocks_json],
                                          key=lambda b: b.index)

                if 'transaction' in result and self._vm_state is VMState.HALT:
                    block = self.current_block
                    if block is None:
                        block = self.increase_block(self.height)

                    tx = Transaction.from_json(result['transaction'])
                    block.add_transaction(tx)

        except BaseException as e:
            self._error_message = str(e)

        # TODO: convert the result to the return type of the function in the manifest
        return self._result_stack[-1] if len(self._result_stack) > 0 else VoidType

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._notifications = []
        self._accounts = []
        self._error_message = None

    def reset_engine(self):
        self.reset_state()
        self._storage.clear()

    def to_json(self, path: Union[str, UInt160], method: str, *args: Any) -> Dict[str, Any]:
        return {
            'path': path if isinstance(path, str) else '',
            'scripthash': str(path) if isinstance(path, UInt160) else None,
            'method': method,
            'arguments': [contract_parameter_to_json(x) for x in args],
            'storage': self._storage.to_json(),
            'contracts': [{'nef': contract_path} for contract_path in self._contract_paths],
            'signerAccounts': [to_hex_str(address) for address in self._accounts],
            'height': self.height,
            'blocks': [block.to_json() for block in self.blocks]
        }
