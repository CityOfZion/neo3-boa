from typing import Any, Dict

from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classtype import ClassType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.bytestype import BytesType
from boa3.model.variable import Variable
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
    def variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Method:
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


_UInt160 = UInt160Type()
