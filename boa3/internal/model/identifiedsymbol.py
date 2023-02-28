from abc import ABC

from boa3.internal.model.symbol import ISymbol


class IdentifiedSymbol(ISymbol, ABC):
    """
    A class to represent a symbol with a name identifier attached to it

    :return: the resulting type when the expression is evaluated
    """

    def __init__(self, identifier: str):
        self._identifier: str = identifier

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
