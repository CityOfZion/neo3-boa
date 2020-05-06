from enum import Enum, EnumMeta

from boa3.model.symbol import ISymbol


class IType(ISymbol):
    def __init__(self, identifier: str):
        self.identifier: str = identifier


class MetaType(EnumMeta, type(IType)):
    """
    Metaclass for the :class:`Type`. Required to construct a Enum with non-builtin value
    """
    pass


class Type(IType, Enum, metaclass=MetaType):
    int = 'int'     # it is the same as `int = IType('int')`
    bool = 'bool'
    str = 'str'
    none = 'none'
