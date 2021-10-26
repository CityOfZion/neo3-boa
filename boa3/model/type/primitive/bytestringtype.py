import abc
from typing import List

from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.neo.vm.type.StackItem import StackItemType


class ByteStringType(SequenceType, PrimitiveType, abc.ABC):
    """
    A class used to represent Neo ByteString type
    """

    def __init__(self, identifier: str, values_type: List[IType]):
        super().__init__(identifier, values_type)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.ByteString

    def _init_class_symbols(self):
        super()._init_class_symbols()

        from boa3.model.builtin.builtin import Builtin

        instance_methods = [Builtin.BytesStringIsDigit,
                            Builtin.BytesStringJoin,
                            Builtin.BytesStringLower,
                            Builtin.BytesStringUpper,
                            Builtin.BytesStringStartswith,
                            Builtin.BytesStringStrip,
                            ]

        for instance_method in instance_methods:
            self._instance_methods[instance_method.raw_identifier] = instance_method.build(self)

    def is_valid_key(self, key_type: IType) -> bool:
        return key_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.model.type.type import Type
        return Type.int

    @property
    def can_reassign_values(self) -> bool:
        return False
