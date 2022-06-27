from typing import Any, List, Optional, Tuple

from boa3 import constants
from boa3.model.method import Method
from boa3.model.type.classes.classtype import ClassType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.bytestype import BytesType
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.AbiType import AbiType


class UInt256Type(BytesType, ClassType):
    """
    A class used to represent Neo's UInt256 type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'UInt256'
        from boa3.model.builtin.method.uint256method import UInt256Method
        self._constructor = UInt256Method(self)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Hash256

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @property
    def default_value(self) -> Any:
        return bytes(constants.SIZE_OF_INT256)

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _UInt256

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, UInt256Type)

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).is_instance_opcodes()

    def _is_instance_inner_opcodes(self, jmp_to_if_false: int = 0) -> List[Tuple[Opcode, bytes]]:
        push_int_opcode, size_data = Opcode.get_push_and_data(constants.SIZE_OF_INT256)

        return [
            (Opcode.SIZE, b''),  # return len(value) == 32
            (push_int_opcode, size_data),
            (Opcode.NUMEQUAL, b'')
        ]


_UInt256 = UInt256Type()
