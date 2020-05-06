from abc import abstractmethod
from enum import Enum

from boa3.model.symbol import ISymbol


class IType(ISymbol):
    def __init__(self, identifier: str):
        self.identifier: str = identifier


class Type(Enum):
    int = IType('int')
    bool = IType('bool')
    str = IType('str')
    none = IType('none')

    @property
    def symbol(self) -> IType:
        return self.value
