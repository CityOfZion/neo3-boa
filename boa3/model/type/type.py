from typing import Dict, Any

from boa3.model.type.anytype import anyType
from boa3.model.type.booltype import BoolType
from boa3.model.type.genericsequencetype import GenericSequenceType
from boa3.model.type.inttype import IntType
from boa3.model.type.itype import IType
from boa3.model.type.listtype import ListType
from boa3.model.type.nonetype import NoneType
from boa3.model.type.strtype import StrType
from boa3.model.type.tupletype import TupleType


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

    # Primitive Types
    int = IntType()
    bool = BoolType()
    str = StrType()
    none = NoneType()
    tuple = TupleType()
    list = ListType()

    # Generic types
    sequence = GenericSequenceType()
    any = anyType
