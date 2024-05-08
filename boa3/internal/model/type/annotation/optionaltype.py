from collections.abc import Iterable
from typing import Any

from boa3.internal.model.type.annotation.uniontype import UnionType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.nonetype import noneType


class OptionalType(UnionType):
    """
    An class used to represent Python Optional annotation type
    """

    def __init__(self, optional_types: set[IType] = None):
        if optional_types is None:
            union_types = None
        else:
            union_types = optional_types.copy()
            if noneType in optional_types:
                optional_types.remove(noneType)
            else:
                union_types.add(noneType)

        super().__init__(union_types)
        self._identifier = 'Optional'
        self._optional_type = optional_types if optional_types is not None else set()

    @property
    def identifier(self) -> str:
        return '{0}[{1}]'.format(self._identifier,
                                 ', '.join([t.identifier for t in self._optional_type]))

    @property
    def optional_types(self) -> list[IType]:
        return list(self._optional_type)

    def _is_type_of(self, value: Any) -> bool:
        if not isinstance(self._optional_type, Iterable) or len(self._optional_type) == 0:
            return False
        if isinstance(value, UnionType):
            return all(self._is_type_of(x) for x in value._union_types)
        return any(t.is_type_of(value) for t in self._union_types)

    @classmethod
    def build(cls, value: Any) -> IType:
        if isinstance(value, Iterable):
            value = set(value)
        else:
            value = {value}
        value.add(noneType)
        return super().build(value)
