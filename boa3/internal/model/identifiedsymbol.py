from abc import ABC

from boa3.internal.model.symbol import ISymbol


class IdentifiedSymbol(ISymbol, ABC):
    """
    A class to represent a symbol with a name identifier attached to it

    :return: the resulting type when the expression is evaluated
    """

    def __init__(self, identifier: str, deprecated: bool = False, new_location: str = None):
        self._identifier: str = identifier
        self._deprecated: bool = deprecated
        self._new_location: str = new_location

    @property
    def identifier(self) -> str:
        """
        Gets the type of the evaluated expression

        :return: the resulting type when the expression is evaluated
        """
        return str(self._identifier)

    @property
    def raw_identifier(self) -> str:
        """
        Gets the type's simple id of the evaluated expression

        :return: the simple id of the resulting type when the expression is evaluated
        """
        return self._identifier

    @property
    def is_deprecated(self) -> bool:
        return self._deprecated

    def deprecate(self, new_location: str = None):
        self._deprecated = True
        if new_location is not None:
            self._new_location = new_location

    @property
    def new_location(self) -> str | None:
        return self._new_location
