from typing import Dict

from boa3.model.symbol import ISymbol


class SymbolScope:
    def __init__(self, symbols: Dict[str, ISymbol] = None):
        self._symbols = symbols.copy() if symbols is not None else {}

    def copy(self):
        return SymbolScope(self._symbols)

    def __getitem__(self, item: str) -> ISymbol:
        return self._symbols[item]

    def __contains__(self, item: str) -> bool:
        return item in self._symbols
