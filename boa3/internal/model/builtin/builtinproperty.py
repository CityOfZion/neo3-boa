from abc import ABC

from boa3.internal.model.builtin.builtinsymbol import IBuiltinSymbol
from boa3.internal.model.method import Method
from boa3.internal.model.property import Property


class IBuiltinProperty(Property, IBuiltinSymbol, ABC):
    def __init__(self,
                 identifier: str,
                 getter: Method,
                 setter: Method = None,
                 deprecated: bool = False
                 ):
        super().__init__(getter, setter, deprecated=deprecated)
        self._identifier = identifier

    def update_with_analyser(self, analyser):
        super().update_with_analyser(analyser)

        if hasattr(self._getter, 'update_with_analyser'):
            self._getter.update_with_analyser(analyser)

        if hasattr(self._setter, 'update_with_analyser'):
            self._setter.update_with_analyser(analyser)
