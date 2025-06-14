from typing import Any

from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.neo3.contracts import TriggerType as Trigger


class TriggerType(IntType):
    """
    A class used to represent Neo interop Trigger type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'TriggerType'

    @property
    def default_value(self) -> Any:
        return Trigger.ALL

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.internal.model.builtin.interop.interop import Interop
            return Interop.TriggerType

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, (Trigger, TriggerType))

    @property
    def symbols(self) -> dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.internal.model.variable import Variable

        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in Trigger.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            return Trigger.__members__[symbol_id]

        return None
