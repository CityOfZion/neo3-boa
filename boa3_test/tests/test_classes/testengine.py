from typing import Any, Dict, List, Optional, Union

from boa3.neo import to_hex_str
from boa3.neo.smart_contract.notification import Notification
from boa3.neo.utils import bytes_from_json, contract_parameter_to_json, stack_item_from_json
from boa3.neo.vm.type.String import String
from boa3.neo3.vm import VMState


class TestEngine:
    def __init__(self, root_path: str):
        self._test_engine_path = '{0}/Neo.TestEngine/Neo.TestEngine.dll'.format(root_path)

        self._vm_state: VMState = VMState.NONE
        self._gas_consumed: int = 0
        self._result_stack: List[Any] = []

        self._storage: Dict[bytes, Any] = {}
        self._notifications: List[Notification] = []

        self._accounts: List[bytes] = []
        self._contract_paths: List[str] = []

        self._error_message: Optional[str] = None

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
    def storage(self) -> Dict[bytes, Any]:
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

    def add_signer_account(self, account: bytes):
        if account not in self._accounts:
            self._accounts.append(account)

    @property
    def contracts(self) -> List[str]:
        return self._contract_paths.copy()

    def add_contract(self, contract_nef_path: str):
        if contract_nef_path.endswith('.nef') and contract_nef_path not in self._contract_paths:
            self._contract_paths.append(contract_nef_path)

    def run(self, nef_path: str, method: str, *arguments: Any, reset_engine: bool = False) -> Any:
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
                if not isinstance(json_storage, list):
                    json_storage = [json_storage]

                storage: Dict[bytes, Any] = {}
                for storage_pair in json_storage:
                    if not isinstance(storage_pair, dict) or list(storage_pair.keys()) != ['key', 'value']:
                        continue

                    key = bytes_from_json(storage_pair['key'])
                    value = bytes_from_json(storage_pair['value'])

                    if isinstance(key, bytes):
                        storage[key] = value if isinstance(value, bytes) else b''

                self._storage = storage

        except BaseException as e:
            self._error_message = str(e)

        # TODO: convert the result to the return type of the function in the manifest
        return self._result_stack[-1] if len(self._result_stack) > 0 else None

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._notifications = []
        self._accounts = []
        self._error_message = None

    def reset_engine(self):
        self.reset_state()
        self._storage = {}

    def to_json(self, path: str, method: str, *args: Any) -> Dict[str, Any]:
        return {
            'path': path,
            'method': method,
            'arguments': [contract_parameter_to_json(x) for x in args],
            'storage': [{'key': contract_parameter_to_json(key),
                         'value': contract_parameter_to_json(value)
                         } for key, value in self._storage.items()],
            'contracts': [{'nef': contract_path} for contract_path in self._contract_paths],
            "signerAccounts": [to_hex_str(address) for address in self._accounts]
        }
