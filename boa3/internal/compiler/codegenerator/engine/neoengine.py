__all__ = [
    'NeoEngine',
    'NeoEngineState'
]

from typing import Any

from boa3.internal.compiler.codegenerator.engine.executionscript import ExecutionScript
from boa3.internal.compiler.codegenerator.engine.istack import IStack
from boa3.internal.neo.vm.VMCode import VMCode
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo3.vm import VMState


class StackItem:
    def __init__(self, value: Any, stack_item_type: StackItemType):
        self.value = value
        self.type = stack_item_type


class NeoStack(IStack):
    def __init__(self):
        super().__init__(stack_type=StackItem)

    def _default_constructor_args(self) -> tuple:
        return tuple()


class NeoEngineState:
    def __init__(self,
                 entry_point: int,
                 ):

        self.entry_point: int = entry_point
        self.current_instruction: int = entry_point
        self.result_stack: list[IStack] = []
        self.vm_state: VMState = VMState.NONE


class NeoEngine:
    def __init__(self):
        self._script: ExecutionScript = None
        self._state_stack: list[NeoEngineState] = []

    @property
    def current_state(self) -> NeoEngineState | None:
        if self._state_stack:
            return self._state_stack[-1]
        else:
            return None

    def load_script(self, script: ExecutionScript):
        self._script = script

    def execute(self, entry_point: int) -> set[int]:
        executed_instructions_addresses = set()

        if not isinstance(self._script, ExecutionScript):
            raise ValueError('Script was not loaded')

        if entry_point not in self._script:
            raise ValueError('Invalid address given as entry point')

        cur_address = entry_point
        self._state_stack.append(NeoEngineState(cur_address))
        while self._state_stack and cur_address in self._script:
            self._execute_instruction(self._script.get_instruction(cur_address))

            executed_instructions_addresses.add(cur_address)
            cur_address = self._script.next_address(cur_address)

        if self._state_stack:
            self._state_stack.clear()

        return executed_instructions_addresses

    def _execute_instruction(self, current_opcode: VMCode):
        match current_opcode.opcode:
            case Opcode.INITSLOT | Opcode.INITSSLOT:
                print()
            case Opcode.RET:
                self._state_stack.pop()
