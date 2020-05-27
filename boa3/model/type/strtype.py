from typing import Any

from boa3.model.type.itype import IType
from boa3.model.type.sequencetype import SequenceType
from boa3.neo.vm.type.AbiType import AbiType


class StrType(SequenceType):
    """
    A class used to represent Python str type
    """

    def __init__(self):
        identifier = 'str'
        super().__init__(identifier, [self])

    @property
    def abi_type(self) -> AbiType:
        return AbiType.String

    @classmethod
    def build(cls, value: Any):
        if cls.is_type_of(value):
            from boa3.model.type.type import Type
            return Type.str

    @classmethod
    def build_sequence(cls, value_type: IType):
        from boa3.model.type.type import Type
        return Type.str

    @classmethod
    def is_type_of(cls, value: Any):
        return type(value) in [str, StrType]

    def is_valid_key(self, value_type: IType) -> bool:
        return value_type == self.valid_key

    @property
    def valid_key(self) -> IType:
        from boa3.model.type.type import Type
        return Type.int
