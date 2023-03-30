from typing import Any

from boa3.internal.model.type.itype import IType


class BaseExceptionType(IType):
    """
    An class used to represent a generic Python exception
    """

    def __init__(self):
        identifier: str = 'exception'
        super().__init__(identifier)

    @property
    def is_generic(self) -> bool:
        return True

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            return cls()

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, BaseExceptionType)

    def __hash__(self):
        return hash(self.identifier)
