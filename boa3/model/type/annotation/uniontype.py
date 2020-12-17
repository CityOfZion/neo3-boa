from typing import Any, Iterable, Set

from boa3.model.type.itype import IType


class UnionType(IType):
    """
    An class used to represent Python Union annotation type
    """

    def __init__(self, union_types: Set[IType] = None):
        identifier: str = 'Union'
        super().__init__(identifier)
        self._union_types: Set[IType] = union_types

    @property
    def identifier(self) -> str:
        return '{0}[{1}]'.format(self._identifier,
                                 ', '.join([t.identifier for t in self._union_types]))

    def _is_type_of(self, value: Any) -> bool:
        if not isinstance(self._union_types, Iterable):
            return False
        return any(t.is_type_of(value) for t in self._union_types)

    @classmethod
    def build(cls, value: Any):
        if isinstance(value, Iterable):
            types = set(value)
        else:
            types = {value}

        if all(isinstance(t, IType) for t in types):
            if len(types) == 1:
                return list(types)[0]
            return cls(types)
