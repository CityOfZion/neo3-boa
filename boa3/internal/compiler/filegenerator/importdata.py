from typing import Dict

from boa3.internal.model.symbol import ISymbol


class ImportData:
    def __init__(self, import_symbol: ISymbol, origin_id: str, origin_file: str = None):
        self._imported_symbol = import_symbol
        self._origin_id = origin_id
        self._origin_file = origin_file

    @property
    def origin(self) -> str:
        if self._origin_id is not None:
            return self._origin_id

        if hasattr(self._imported_symbol, 'origin'):
            return self._imported_symbol.origin

        return None

    @property
    def origin_file(self) -> str:
        return self._origin_file

    @property
    def all_symbols(self) -> Dict[str, ISymbol]:
        if hasattr(self._imported_symbol, 'all_symbols'):
            return self._imported_symbol.all_symbols

        if hasattr(self._imported_symbol, 'symbols'):
            return self._imported_symbol.symbols

        return {}
