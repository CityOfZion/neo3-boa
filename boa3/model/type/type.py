from typing import Dict, Any

from boa3.model.type.anytype import anyType
from boa3.model.type.itype import IType
from boa3.model.type.primitive.booltype import BoolType
from boa3.model.type.primitive.inttype import IntType
from boa3.model.type.primitive.nonetype import NoneType
from boa3.model.type.primitive.strtype import StrType
from boa3.model.type.sequence.genericsequencetype import GenericSequenceType
from boa3.model.type.sequence.mutable.genericmutablesequencetype import GenericMutableSequenceType
from boa3.model.type.sequence.mutable.listtype import ListType
from boa3.model.type.sequence.tupletype import TupleType


class Type:
    @classmethod
    def values(cls) -> Dict[str, IType]:
        value_dict = {}
        for type in vars(cls).values():
            if isinstance(type, IType):
                value_dict[type._identifier] = type
        return value_dict

    @classmethod
    def get_type(cls, value: Any) -> IType:
        """
        Returns the type of the given value.

        :param value: value to get the type
        :return: Returns the type of the value. `Type.none` by default.
        """
        val: IType = None
        for type in vars(cls).values():
            if isinstance(type, IType) and type.is_type_of(value):
                val = type.build(value)
                break

        if val is not None:
            return val
        return cls.none

    @classmethod
    def get_generic_type(cls, type1: IType, type2: IType) -> IType:
        """
        Returns the common generic type between the given values.

        :param type1: first type to be compared
        :param type2: second type to be compared
        :return: Returns the common generic type of the values if exist. `Type.any` otherwise.
        """
        if type1 == type2 or type1.is_type_of(type2):
            return type1
        if type2.is_type_of(type1):
            return type2

        generic_types = [cls.mutableSequence, cls.sequence]
        for generic in generic_types:
            if generic.is_type_of(type1) and generic.is_type_of(type2):
                return generic
        return Type.any

    # Primitive Types
    int = IntType()
    bool = BoolType()
    str = StrType()
    none = NoneType()
    tuple = TupleType()
    list = ListType()

    # Generic types
    sequence = GenericSequenceType()
    mutableSequence = GenericMutableSequenceType()
    any = anyType
