from __future__ import annotations

__all__ = [
    'ExecutionScript'
]


from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
from boa3.internal.neo.vm.VMCode import VMCode
from boa3.internal.neo3.contracts.nef import MethodToken


class ExecutionScript:
    def __init__(self, code_map: dict[int, VMCode], tokens: list[MethodToken]):
        self._addresses = tuple(code_map.keys())
        self._instructions = tuple(code_map.values())

        self._last_address = self._addresses[-1] if len(self._addresses) else -1
        self._last_instruction_size = self._instructions[-1].size if len(self._instructions) else 0

        self._tokens = tokens

    @classmethod
    def from_code_map(cls, instance: VMCodeMapping) -> ExecutionScript:
        obj = ExecutionScript(instance.code_map, instance._method_tokens.to_list())
        return obj

    def get_instruction(self, address) -> VMCode:
        if address not in self._addresses:
            raise IndexError
        index = self._addresses.index(address)
        return self._instructions[index]

    def next_address(self, address) -> int:
        if address in self._addresses:
            address_index = self._addresses.index(address)
            if address < self._last_address:
                next_address = self._addresses[address_index + 1]
            else:
                next_address = self._last_address + self._last_instruction_size
        else:
            next_address = next((instr_address
                                 for instr_address in self._addresses
                                 if instr_address > address),
                                self._last_address + self._last_instruction_size)

        return next_address

    def __contains__(self, obj) -> bool:
        return obj in self._addresses
