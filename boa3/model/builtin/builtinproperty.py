from abc import ABC

from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.method import Method
from boa3.model.property import Property


class IBuiltinProperty(Property, IdentifiedSymbol, ABC):
    def __init__(self, identifier: str, getter: Method, setter: Method = None):
        super().__init__(getter, setter)
        self._identifier = identifier
