from typing import Any, List, Tuple

from boa3.model.type.itype import IType
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.AbiType import AbiType


class __AnyType(IType):
    """
    A class used to represent Python bool type
    """

    def __init__(self):
        identifier = 'any'
        super().__init__(identifier)

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Any

    @classmethod
    def build(cls, value: Any) -> IType:
        from boa3.model.type.type import Type
        return Type.any

    @classmethod
    def _is_type_of(cls, value: Any):
        return True

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.PUSH1, b'')]  # any is type of everything, so inserts True


anyType: IType = __AnyType()
