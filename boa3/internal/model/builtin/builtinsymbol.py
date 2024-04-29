from abc import ABC
from typing import Self

from boa3.internal.model.identifiedsymbol import IdentifiedSymbol


class IBuiltinSymbol(IdentifiedSymbol, ABC):

    def build(self, *args, **kwargs) -> Self:
        """
        Creates a symbol instance with the given value as self

        :return: The built method if the value is valid. The current object otherwise
        :rtype: IBuiltinSymbol
        """
        return self

    def update_with_analyser(self, analyser):
        return
