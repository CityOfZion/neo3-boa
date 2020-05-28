from abc import ABC
from typing import Optional


class CompilerWarning(ABC):
    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col

    @property
    def message(self) -> str:
        message = '' if self._warning_message is None else ' - ' + self._warning_message
        return '{0}:{1}{2}'.format(self.line, self.col, message)

    @property
    def _warning_message(self) -> Optional[str]:
        return None

    def __str__(self) -> str:
        return self.message


class NameShadowing(CompilerWarning):
    """
    An warning raised when a name from an outer scope symbol is used as the name of an inner scope symbol
    """
    from boa3.model.symbol import ISymbol

    def __init__(self, line: int, col: int, outer_symbol: ISymbol, symbol_id: str):
        self.symbol_id: str = symbol_id
        self.existing_symbol = outer_symbol
        super().__init__(line, col)

    @property
    def _warning_message(self) -> Optional[str]:
        if self.symbol_id is not None:
            return "Shadowing {0} name '{1}'".format(self.existing_symbol.shadowing_name, self.symbol_id)
