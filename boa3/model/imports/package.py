from __future__ import annotations

from typing import Dict, List, Optional

from boa3.model.identifiedsymbol import IdentifiedSymbol


class Package(IdentifiedSymbol):
    """
    A class used to represent a Python module.

    :ivar properties: a list that stores every property in the package. Empty by default.
    :ivar methods: a list that stores every method in the package. Empty by default.
    :ivar types: a list that stores every property in the package. Empty by default.
    """

    def __init__(self, identifier: str,
                 properties: List[IdentifiedSymbol] = None,
                 methods: List[IdentifiedSymbol] = None,
                 types: List[IdentifiedSymbol] = None,
                 packages: List[Package] = None
                 ):
        from enum import Enum
        if isinstance(identifier, Enum):
            identifier = identifier.value

        super().__init__(identifier)

        self._all_symbols: List[IdentifiedSymbol] = []

        if methods is None:
            methods = []
        self._all_symbols.extend(methods)

        if properties is None:
            properties = []
        self._all_symbols.extend(properties)

        if types is None:
            types = []
        self._all_symbols.extend(types)

        if packages is None:
            packages = []
        for package in packages:
            self._all_symbols.append(package)
            package._parent = self

        self._aliases: Dict[str, str] = {}
        self._parent: Optional[Package] = None

    @property
    def shadowing_name(self) -> str:
        return 'package'

    @property
    def symbols(self) -> Dict[str, IdentifiedSymbol]:
        """
        Gets all the symbols in the package.

        :return: a list that stores every symbol in the package
        """
        return {(self._aliases[symbol.raw_identifier]
                 if symbol.raw_identifier in self._aliases
                 else symbol.raw_identifier): symbol
                for symbol in self._all_symbols}

    @property
    def parent(self) -> Optional[Package]:
        """
        Get the parent package of this one. None if it's the root package.
        """
        return self._parent

    def include_symbol(self, symbol_id, symbol: IdentifiedSymbol):
        identifier = symbol.raw_identifier if isinstance(symbol, IdentifiedSymbol) else symbol_id
        if all(package_symbol.raw_identifier != identifier for package_symbol in self._all_symbols):
            if isinstance(symbol, IdentifiedSymbol) and symbol.raw_identifier != symbol_id:
                self._aliases[symbol.raw_identifier] = symbol_id

            if isinstance(symbol, Package):
                if symbol._parent is not None:
                    return
                symbol._parent = self
            self._all_symbols.append(symbol)

    def __repr__(self) -> str:
        return self.identifier
