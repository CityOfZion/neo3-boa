from typing import Any, Dict, List, Optional, Tuple

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classtype import ClassType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.bytestype import BytesType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItem import StackItemType


class UInt160Type(BytesType, ClassType):
    """
    A class used to represent Neo's UInt160 type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'UInt160'
        from boa3.model.builtin.method.uint160method import UInt160Method
        self._constructor = UInt160Method(self)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Hash160

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.ByteString

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @property
    def default_value(self) -> Any:
        return bytes(20)

    @classmethod
    def build(cls, value: Any = None) -> IType:
        return _UInt160

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, UInt160Type)

    def _is_instance_inner_opcodes(self, jmp_to_if_false: int = 0) -> List[Tuple[Opcode, bytes]]:
        push_int_opcode, size_data = Opcode.get_push_and_data(20)

        return [
            (Opcode.SIZE, b''),  # return len(value) == 20
            (push_int_opcode, size_data),
            (Opcode.NUMEQUAL, b'')
        ]


_UInt160 = UInt160Type()
