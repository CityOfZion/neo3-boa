from __future__ import annotations

from typing import Dict, List, Optional

from boa3.internal.model.identifiedsymbol import IdentifiedSymbol


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
                 packages: List[Package] = None,
                 other_symbols: dict = None,
                 import_origin=None
                 ):
        """
        :param packages: a list that stores the inner packages and modules of this package. Empty by default.
        :param other_symbols: a dictionary with other symbols that are evaluated during the compilation. Empty by
          default. Should be None for builtin packages.
        :type other_symbols: dict or None
        :param import_origin: the analyser that generated this package. Should be None for builtin packages.
        :type import_origin: boa3.internal.model.imports.importsymbol.Import
        """

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
        self._packages = packages
        for package in packages:
            package._parent = self

        # for packages that are not builtin
        if isinstance(other_symbols, dict):
            from boa3.internal.model.symbol import ISymbol
            self._additional_symbols = {key: value
                                        for key, value in other_symbols.items()
                                        if (value not in self._all_symbols
                                            and isinstance(key, str)
                                            and isinstance(value, ISymbol))}
            self.origin = import_origin
        else:
            self._additional_symbols = {}
            self.origin = None

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
        symbol_map = {(self._aliases[symbol.raw_identifier]
                       if symbol.raw_identifier in self._aliases
                       else symbol.raw_identifier): symbol
                      for symbol in self._all_symbols}
        symbol_map.update(self._additional_symbols)
        return symbol_map

    @property
    def inner_packages(self) -> Dict[str, Package]:
        return {symbol.raw_identifier: symbol for symbol in self._packages}

    @property
    def parent(self) -> Optional[Package]:
        """
        Get the parent package of this one. None if it's the root package.
        """
        return self._parent

    def include_symbol(self, symbol_id, symbol: IdentifiedSymbol):
        identifier = symbol.raw_identifier if isinstance(symbol, IdentifiedSymbol) else symbol_id
        check_list = self._packages if isinstance(symbol, Package) else self._all_symbols

        if all(package_symbol.raw_identifier != identifier for package_symbol in check_list):
            if isinstance(symbol, IdentifiedSymbol) and symbol.raw_identifier != symbol_id:
                self._aliases[symbol.raw_identifier] = symbol_id

            if isinstance(symbol, Package):
                self._packages.append(symbol)
                if symbol._parent is not None:
                    return
                symbol._parent = self
            else:
                self._all_symbols.append(symbol)

    def update_with_analyser(self, analyser):
        from boa3.internal.analyser.analyser import Analyser
        if isinstance(analyser, Analyser):
            for symbol in self._all_symbols:
                if hasattr(symbol, 'update_with_analyser'):
                    symbol.update_with_analyser(analyser)
            for pkg in self._packages:
                pkg.update_with_analyser(analyser)

    def __repr__(self) -> str:
        return self.identifier
