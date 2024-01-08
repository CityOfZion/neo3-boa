__all__ = [
    'StrType', 'StrBufferType'
]

from typing import Any

from boa3.internal import constants
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class StrType(IByteStringType):
    """
    A class used to represent Python str type
    """

    def __init__(self):
        identifier = 'str'
        super().__init__(identifier, [self])

    @property
    def default_value(self) -> Any:
        return str()

    @property
    def abi_type(self) -> AbiType:
        return AbiType.String

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.internal.model.builtin.builtin import Builtin

        instance_methods = [Builtin.StrSplit,
                            Builtin.BytesStringIndex,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

        self._instance_methods[constants.INIT_METHOD_ID] = Builtin.StrBytes

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.type.type import Type
            return Type.str

    @classmethod
    def build_collection(cls, value_type: IType):
        from boa3.internal.model.type.type import Type
        return Type.str

    @classmethod
    def _is_type_of(cls, value: Any) -> bool:
        from boa3.internal.model.type.collection.sequence.buffertype import BufferType
        return isinstance(value, (str, StrType)) and not isinstance(value, BufferType)

    def is_type_of(self, value: Any) -> bool:
        return self._is_type_of(value)


class StrBufferType(StrType):
    """
    This class is used to represent Python str type on operations that internally use Neo Buffer type
    """
    def __init__(self):
        super().__init__()

    def stack_item(self) -> StackItemType:
        return StackItemType.Buffer

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.type.type import Type
            return Type.bufferStr

    @classmethod
    def build_collection(cls, value_type: IType):
        from boa3.internal.model.type.type import Type
        return Type.bufferStr

    @classmethod
    def _is_type_of(cls, value: Any) -> bool:
        if isinstance(value, (str, StrBufferType)):
            return True
        return super()._is_type_of(value)
