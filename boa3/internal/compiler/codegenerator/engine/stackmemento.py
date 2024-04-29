__all__ = [
    'StackMemento',
    'NeoStack'
]

from boa3.internal.compiler.codegenerator.engine.istack import IStack
from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.VMCode import VMCode


class NeoStack(IStack):
    def __init__(self):
        from boa3.internal.model.type.itype import IType
        super().__init__(stack_type=IType)

    def _default_constructor_args(self) -> tuple:
        return tuple()


class StackMemento:
    """
    This class is responsible for managing the simulation of the blockchain stack during the code generation
    """

    def __init__(self):
        self._stacks: list[tuple[VMCode, NeoStack]] = []
        self._current_stack: NeoStack = NeoStack()

    @property
    def stack_map(self) -> dict[int, NeoStack]:
        vm_code_mapping = VMCodeMapping.instance()
        return {vm_code_mapping.get_start_address(vmcode): stack for vmcode, stack in self._stacks}

    def get_state(self, code_address: int) -> NeoStack:
        stacks = self.stack_map
        index = None
        for address, stack in sorted(stacks.items()):
            if address >= code_address:
                break
            index = address

        if index is None or index not in stacks:
            return NeoStack()
        else:
            return stacks[index]

    @property
    def current_stack(self) -> NeoStack:
        return self._current_stack

    def restore_state(self, code_address):
        stacks = self.stack_map
        latest_stack = None
        for address, stack in reversed(sorted(stacks.items())):
            if address < code_address:
                latest_stack = stack
                break

            vm_code = VMCodeMapping.instance().get_code(address)
            if (vm_code, stack) in self._stacks:
                self._stacks.remove((vm_code, stack))

        if latest_stack is not None:
            self._current_stack = latest_stack

    def append(self, code: VMCode, value: IType):
        states = self.stack_map
        index = VMCodeMapping.instance().get_start_address(code)
        if index in states:
            states[index].append(value)

        else:
            if self._current_stack is not None:
                stack = self._current_stack.copy()
            else:
                stack = NeoStack()
            stack.append(value)

            self._stacks.append((code, stack))
            self._current_stack = stack

    def pop(self, code: VMCode, index: int = -1):
        states = self.stack_map
        stack_index = VMCodeMapping.instance().get_start_address(code)
        if stack_index in states:
            stack = states[stack_index]
        else:
            if self._current_stack is not None:
                stack = self._current_stack.copy()
            else:
                stack = NeoStack()

            self._stacks.append((code, stack))
            self._current_stack = stack

        if len(stack) > 0:
            return stack.pop(index)

    def reverse(self, code: VMCode, start: int = 0, end: int = None, *, rotate: bool = False):
        states = self.stack_map
        stack_index = VMCodeMapping.instance().get_start_address(code)
        if stack_index in states:
            stack = states[stack_index]
        else:
            if self._current_stack is not None:
                stack = self._current_stack.copy()
            else:
                stack = NeoStack()

            self._stacks.append((code, stack))
            self._current_stack = stack

        return stack.reverse(start, end, rotate=rotate)
