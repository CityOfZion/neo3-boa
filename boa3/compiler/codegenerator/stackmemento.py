from __future__ import annotations

from typing import Dict, List, Tuple, Union

from boa3.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.model.type.itype import IType
from boa3.neo.vm.VMCode import VMCode


class StackMemento:
    """
    This class is responsible for managing the simulation of the blockchain stack during the code generation
    """

    def __init__(self):
        self._stacks: List[Tuple[VMCode, NeoStack]] = []
        self._current_stack: NeoStack = NeoStack()

    @property
    def stack_map(self) -> Dict[int, NeoStack]:
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

    def append(self, value: IType, code: VMCode):
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


class NeoStack:
    def __init__(self):
        self._stack: List[IType] = []

    def append(self, value: IType):
        return self._stack.append(value)

    def clear(self):
        return self._stack.clear()

    def copy(self) -> NeoStack:
        new_stack = NeoStack()
        new_stack._stack = self._stack.copy()
        return new_stack

    def pop(self, index: int) -> IType:
        return self._stack.pop(index)

    def __len__(self) -> int:
        return len(self._stack)

    def __getitem__(self, index_or_slice: Union[int, slice]):
        return self._stack[index_or_slice]

    def reverse(self, start: int = 0, end: int = None):
        if end is None:
            end = len(self._stack)

        reverse = list(reversed(self._stack[start:end]))
        self._stack[start:end] = reverse
