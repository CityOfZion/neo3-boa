from __future__ import annotations

from typing import Any, Dict

from boa3.model.symbol import ISymbol
from boa3.model.type.primitive.inttype import IntType
from boa3.neo3.vm import VMState


class VMStateType(IntType):
    """
    A class used to represent Neo interop VMState type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'VMState'

    @property
    def default_value(self) -> Any:
        return VMState.NONE

    @classmethod
    def build(cls, value: Any = None) -> VMStateType:
        if value is None or cls._is_type_of(value):
            return _VMState

    @classmethod
    def _is_type_of(cls, value: Any = None):
        return isinstance(value, (VMState, VMStateType))

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        """
        Gets the class symbols of this type

        :return: a dictionary that maps each symbol in the module with its name
        """
        from boa3.model.variable import Variable

        _symbols = super().symbols
        _symbols.update({name: Variable(self) for name in VMState.__members__.keys()})

        return _symbols

    def get_value(self, symbol_id) -> Any:
        """
        Gets the literal value of a symbol

        :return: the value if this type has this symbol. None otherwise.
        """
        if symbol_id in self.symbols:
            return VMState.__members__[symbol_id]

        return None


_VMState = VMStateType()