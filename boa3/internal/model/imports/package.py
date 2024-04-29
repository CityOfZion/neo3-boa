from typing import Self

from boa3.internal.model.identifiedsymbol import IdentifiedSymbol


class Package(IdentifiedSymbol):
    """
    A class used to represent a Python module.

    :ivar properties: a list that stores every property in the package. Empty by default.
    :ivar methods: a list that stores every method in the package. Empty by default.
    :ivar types: a list that stores every property in the package. Empty by default.
    """

    @classmethod
    def create_package(
            cls,
            package_id: str,
            symbols: dict[str, IdentifiedSymbol] = None,
    ) -> Self:

        from boa3.internal import constants
        package_ids = package_id.split(constants.ATTRIBUTE_NAME_SEPARATOR)
        pkg = Package(identifier=package_ids[-1], other_symbols=symbols)
        for pkg_id in reversed(package_ids[:-1]):
            pkg = Package(identifier=pkg_id, packages=[pkg])
        return pkg

    def __init__(self,
                 identifier: str,
                 properties: list[IdentifiedSymbol] = None,
                 methods: list[IdentifiedSymbol] = None,
                 types: list[IdentifiedSymbol] = None,
                 packages: list[Self] = None,
                 other_symbols: dict = None,
                 import_origin=None,
                 deprecated: bool = False,
                 new_location: str = None
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

        self._all_symbols: list[IdentifiedSymbol] = []

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

        self._aliases: dict[str, str] = {}
        self._parent: Self | None = None

        if deprecated:
            self.deprecate(new_location)

    @property
    def shadowing_name(self) -> str:
        return 'package'

    @property
    def symbols(self) -> dict[str, IdentifiedSymbol]:
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
    def inner_packages(self) -> dict[str, Self]:
        return {symbol.raw_identifier: symbol for symbol in self._packages}

    @property
    def parent(self) -> Self | None:
        """
        Get the parent package of this one. None if it's the root package.
        """
        return self._parent

    def deprecate(self, new_location: str = None):
        if not self._deprecated:
            from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
            if new_location is not None:
                self._new_location = new_location
            elif self._parent is not None and self._parent.new_location is not None:
                from boa3.internal import constants
                self._new_location = constants.ATTRIBUTE_NAME_SEPARATOR.join(
                    (self._parent.new_location, self.identifier)
                )

            self._deprecated = True
            for index, symbol in enumerate(self._all_symbols):
                deprecated_symbol = symbol.clone()
                if (self.new_location is not None
                        and isinstance(deprecated_symbol, IBuiltinCallable)
                        and deprecated_symbol.new_location is None
                ):
                    deprecated_symbol.set_new_location(self.new_location)

                deprecated_symbol.deprecate()
                self._all_symbols[index] = deprecated_symbol

            for pkg in self._packages:
                pkg.deprecate()

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
                if self.is_deprecated:
                    symbol.deprecate()
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
