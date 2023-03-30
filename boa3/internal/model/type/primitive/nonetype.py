from typing import Any, List, Tuple

from boa3.internal.model.type.classes.pythonclass import PythonClass
from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.AbiType import AbiType


class NoneType(PythonClass):
    """
    A class used to represent Python None value
    """

    def __init__(self):
        identifier = 'none'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Void

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.type.type import Type
            return Type.none

    @classmethod
    def _is_type_of(cls, value: Any):
        from boa3.internal.model.type.type import Type
        return value is None or value is Type.none

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.ISNULL, b'')]


noneType: IType = NoneType()
