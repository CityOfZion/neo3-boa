from __future__ import annotations

from typing import Any, Dict

from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.neo3.network.payloads.verification import WitnessRuleAction


class WitnessRuleActionType(IntType):
    """
    A class used to represent Neo interop WitnessRuleAction type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'WitnessRuleAction'

    @property
    def default_value(self) -> Any:
        return WitnessRuleAction.DENY

    @classmethod
    def build(cls, value: Any = None) -> WitnessRuleActionType:
        if value is None or cls._is_type_of(value):
            return _WitnessRuleAction

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (WitnessRuleAction, WitnessRuleActionType))

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.internal.model.variable import Variable

        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in WitnessRuleAction.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            return WitnessRuleAction.__members__[symbol_id]

        return None


_WitnessRuleAction = WitnessRuleActionType()
