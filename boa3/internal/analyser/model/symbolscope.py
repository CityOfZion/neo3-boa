from typing import Self

from boa3.internal.model.symbol import ISymbol


class SymbolScope:
    def __init__(self, symbols: dict[str, ISymbol] = None):
        self._symbols = symbols.copy() if symbols is not None else {}

    @property
    def symbols(self) -> dict[str, ISymbol]:
        return self._symbols.copy()

    def copy(self) -> Self:
        return SymbolScope(self._symbols)

    def include_symbol(self, symbol_id: str, symbol: ISymbol, reassign_original: bool = True):
        """
        Includes a symbols into the scope

        :param symbol_id: symbol identifier
        :param symbol: symbol to be included
        """

        if symbol_id in self._symbols:
            if not reassign_original:
                if hasattr(symbol, 'copy'):
                    symbol = symbol.copy()
                else:
                    return

            if hasattr(symbol, 'set_is_reassigned'):
                symbol.set_is_reassigned()

        self._symbols[symbol_id] = symbol

    def remove_symbol(self, symbol_id: str):
        """
        Removes a symbols from the scope

        :param symbol_id: symbol identifier
        """
        if symbol_id in self._symbols:
            self._symbols.pop(symbol_id)

    def __getitem__(self, item: str) -> ISymbol:
        return self._symbols[item]

    def __contains__(self, item: str) -> bool:
        return item in self._symbols

    def __repr__(self) -> str:
        return self._symbols.__repr__()
