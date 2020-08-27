from abc import ABC

from boa3.model.symbol import ISymbol


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
        return self._identifier
