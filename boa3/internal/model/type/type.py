from typing import Any

from boa3.internal.model.type.annotation.ellipsistype import ellipsisType
from boa3.internal.model.type.annotation.optionaltype import OptionalType
from boa3.internal.model.type.annotation.uniontype import UnionType
from boa3.internal.model.type.anytype import anyType
from boa3.internal.model.type.baseexceptiontype import BaseExceptionType
from boa3.internal.model.type.collection.genericcollectiontype import GenericCollectionType
from boa3.internal.model.type.collection.mapping.genericmappingtype import GenericMappingType
from boa3.internal.model.type.collection.mapping.mutable.dicttype import DictType
from boa3.internal.model.type.collection.sequence.genericsequencetype import GenericSequenceType
from boa3.internal.model.type.collection.sequence.mutable.genericmutablesequencetype import GenericMutableSequenceType
from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
from boa3.internal.model.type.collection.sequence.rangetype import RangeType
from boa3.internal.model.type.collection.sequence.reversedtype import ReversedType
from boa3.internal.model.type.collection.sequence.tupletype import TupleType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.booltype import BoolType
from boa3.internal.model.type.primitive.bytearraytype import ByteArrayType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.primitive.nonetype import noneType
from boa3.internal.model.type.primitive.strtype import StrType


class Type:
    @classmethod
    def builtin_types(cls) -> dict[str, IType]:
        """
        Gets a dictionary that maps each type with its name

        :return: A dictionary that maps each Python builtin type representation with its name
        """
        builtin_types = [
            Type.int,
            Type.bool,
            Type.str,
            Type.list,
            Type.tuple,
            Type.dict,
            Type.range,
            Type.reversed,
            Type.bytes,
            Type.bytearray,
            Type.none
        ]
        return {tpe._identifier: tpe for tpe in builtin_types if isinstance(tpe, IType)}

    @classmethod
    def all_types(cls) -> dict[str, IType]:
        return {tpe._identifier: tpe for tpe in vars(cls).values() if isinstance(tpe, IType)}

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
    def get_generic_type(cls, *types: IType) -> IType:
        """
        Returns the common generic type between the given values.

        :param types: list of type to be compared
        :return: Returns the common generic type of the values if exist. `Type.any` otherwise.
        """
        generic = cls.any
        if len(types) > 0:
            generic_types = [cls.mutableSequence, cls.mapping, cls.sequence]
            generic_types.append(generic)  # any type must be the last value in the list

            generic = types[0]
            for tpe in types[1:]:
                if generic == tpe or generic.is_type_of(tpe):
                    continue
                if tpe.is_type_of(generic):
                    generic = tpe
                    continue

                for gen in generic_types:
                    if gen.is_type_of(generic) and gen.is_type_of(tpe):
                        generic = gen
                        break

                if generic is Type.any:
                    break
        if generic is Type.any and Type.any not in types:
            generic = Type.union.build(types)
        return generic

    # Builtin Types
    int = IntType()
    bool = BoolType()
    str = StrType()
    none = noneType
    bytes = BytesType()
    bytearray = ByteArrayType()
    tuple = TupleType()
    list = ListType()
    dict = DictType()
    range = RangeType(int)
    reversed = ReversedType()

    # Generic types
    sequence = GenericSequenceType()
    mutableSequence = GenericMutableSequenceType()
    mapping = GenericMappingType()
    collection = GenericCollectionType()
    exception = BaseExceptionType()

    # Annotation types
    union = UnionType()
    optional = OptionalType()
    ellipsis = ellipsisType
    any = anyType
