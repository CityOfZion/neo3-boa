from __future__ import annotations

from typing import Dict

from boa3.model.symbol import ISymbol


class SymbolScope:
    def __init__(self, symbols: Dict[str, ISymbol] = None):
        self._symbols = symbols.copy() if symbols is not None else {}

    @property
    def symbols(self) -> Dict[str, ISymbol]:
        return self._symbols.copy()

    def copy(self) -> SymbolScope:
        return SymbolScope(self._symbols)

    def include_symbol(self, symbol_id: str, symbol: ISymbol):
        """
        Includes a symbols into the scope

        :param symbol_id: method identifier
        :param symbol: method to be included
        """
        self._symbols[symbol_id] = symbol

    def __getitem__(self, item: str) -> ISymbol:
        return self._symbols[item]

    def __contains__(self, item: str) -> bool:
        return item in self._symbols
