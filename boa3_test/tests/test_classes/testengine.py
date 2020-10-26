from typing import Any, Dict, List, Optional, Union

from boa3.neo.smart_contract.notification import Notification
from boa3.neo.utils import contract_parameter_to_json, stack_item_from_json
from boa3.neo.vm.type.String import String
from boa3.neo3.vm import VMState


class TestEngine:
    def __init__(self, root_path: str):
        self._test_engine_path = '{0}/TestEngine/TestEngine.dll'.format(root_path)

        self._vm_state: VMState = VMState.NONE
        self._gas_consumed: int = 0
        self._result_stack: List[Any] = []
        self._storage: Dict[str, Any] = {}
        self._notifications: List[Notification] = []
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
        return self._notifications

    def get_events(self, event_name: str) -> List[Notification]:
        return [n for n in self._notifications if n.name == event_name]

    @property
    def storage(self) -> Dict[str, Any]:
        return self._storage.copy()

    def storage_get(self, key: Union[str, bytes]) -> Any:
        if isinstance(key, bytes):
            key = String.from_bytes(key)

        if key in self._storage:
            return self._storage[key]
        else:
            return None

    def storage_put(self, key: Union[str, bytes], value: Any):
        if isinstance(key, bytes):
            key = String.from_bytes(key)

        self._storage[key] = value

    def storage_delete(self, key: Union[str, bytes]):
        if isinstance(key, bytes):
            key = String.from_bytes(key)

        if key in self._storage:
            self._storage.pop(key)

    def run(self, nef_path: str, method: str, *arguments: Any, reset_engine: bool = False) -> Any:
        import json
        import subprocess

        contract_parameters = [contract_parameter_to_json(x) for x in arguments]
        param_json = json.dumps(contract_parameters).replace(' ', '')

        process = subprocess.Popen(['dotnet', self._test_engine_path, nef_path, method, param_json],
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
                json_notifications = result['notifications']
                if not isinstance(json_notifications, list):
                    json_notifications = [json_notifications]

                notifications = []
                for n in json_notifications:
                    new = Notification.from_json(n)
                    if new is not None:
                        notifications.append(new)
                self._notifications = notifications

        except BaseException as e:
            self._error_message = str(e)

        # TODO: convert the result to the return type of the function in the manifest
        return self._result_stack[-1] if len(self._result_stack) > 0 else None

    def reset_state(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._notifications = []
        self._error_message = None

    def reset_engine(self):
        self._vm_state = VMState.NONE
        self._gas_consumed = 0
        self._result_stack = []
        self._storage = {}
        self._notifications = []
        self._error_message = None
