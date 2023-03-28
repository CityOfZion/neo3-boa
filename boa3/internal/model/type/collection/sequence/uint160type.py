from typing import Any, List, Optional, Tuple

from boa3.internal import constants
from boa3.internal.model.method import Method
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.AbiType import AbiType


class UInt160Type(BytesType):
    """
    A class used to represent Neo's UInt160 type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'UInt160'
        from boa3.internal.model.builtin.method.uint160method import UInt160Method
        self._constructor = UInt160Method(self)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Hash160

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @property
    def default_value(self) -> Any:
        return bytes(constants.SIZE_OF_INT160)

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _UInt160

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, UInt160Type)

    def is_instance_opcodes(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.model.type.classes.pythonclass import PythonClass
        return super(PythonClass, self).is_instance_opcodes()

    def _is_instance_inner_opcodes(self, jmp_to_if_false: int = 0) -> List[Tuple[Opcode, bytes]]:
        push_int_opcode, size_data = OpcodeHelper.get_push_and_data(constants.SIZE_OF_INT160)

        return [
            (Opcode.SIZE, b''),  # return len(value) == 20
            (push_int_opcode, size_data),
            (Opcode.NUMEQUAL, b'')
        ]


_UInt160 = UInt160Type()