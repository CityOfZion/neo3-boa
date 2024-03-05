from collections.abc import Iterable
from typing import Any

from boa3.internal.model.type.itype import IType
from boa3.internal.neo.vm.type.AbiType import AbiType
from boa3.internal.neo.vm.type.StackItem import StackItemType


class UnionType(IType):
    """
    An class used to represent Python Union annotation type
    """

    def __init__(self, union_types: set[IType] = None):
        identifier: str = 'Union'
        super().__init__(identifier)
        self._union_types: set[IType] = union_types if union_types is not None else set()

        # variables to not reevaluate everytime we need to access
        self._abi_type: AbiType = None
        self._stack_item: StackItemType = None

    @property
    def identifier(self) -> str:
        return '{0}[{1}]'.format(self._identifier,
                                 ', '.join([t.identifier for t in self._union_types]))

    @property
    def union_types(self) -> list[IType]:
        return list(self._union_types)

    @property
    def abi_type(self) -> AbiType:
        if self._abi_type is None:
            self._abi_type = AbiType.union([union.abi_type for union in self._union_types])
        return self._abi_type

    @property
    def stack_item(self) -> StackItemType:
        if self._stack_item is None:
            self._stack_item = StackItemType.union([union.stack_item for union in self._union_types])
        return self._stack_item

    def _is_type_of(self, value: Any) -> bool:
        if not isinstance(self._union_types, Iterable) or len(self._union_types) == 0:
            return False
        if isinstance(value, UnionType):
            return all(self._is_type_of(x) for x in value._union_types)
        return any(t.is_type_of(value) for t in self._union_types)

    @classmethod
    def build(cls, value: Any) -> IType:
        if isinstance(value, Iterable):
            types = set(value)
        else:
            types = {value}

        from boa3.internal.model.type.type import Type
        if any(t is Type.any for t in types):
            return Type.any

        if all(isinstance(t, IType) for t in types):
            for x in types.copy():
                if isinstance(x, UnionType):
                    types.remove(x)
                    types = types.union(x._union_types)
            if len(types) == 1:
                return list(types)[0]
            return cls(types)

    def except_type(self, other_type: IType) -> IType:
        """
        Gets a type that is type of `self` but is not type of `other_type`.
        If `other_type` is an implementation of `self`, returns `self`

        :param other_type: type that won't be allowed in the resulting type
        :type other_type: IType
        :return: an union of this type and the exclusion of other_type
        :rtype: IType
        """
        if not self.is_type_of(other_type):
            return self

        new_union = []
        for x in self._union_types:
            if not other_type.is_type_of(x):
                new_union.append(x)

        if len(new_union) < 2:
            from boa3.internal.model.type.type import Type
            return Type.none if len(new_union) == 0 else new_union[0]
        else:
            return UnionType(set(new_union))

    def intersect_type(self, other_type: IType) -> IType:
        if self.is_type_of(other_type):
            return other_type
        if other_type.is_type_of(self):
            return self

        if isinstance(other_type, type(self)):
            other_types = [x for x in other_type.union_types if self.is_type_of(x)]
            self_types = [x for x in self.union_types if other_type.is_type_of(x)]

            common_types = other_types + self_types
            if len(common_types) == 1:
                return common_types[0]
            elif len(common_types) > 1:
                return self.build(common_types)

        return super().intersect_type(other_type)

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other) -> bool:
        return isinstance(other, UnionType) and self._union_types == other._union_types
