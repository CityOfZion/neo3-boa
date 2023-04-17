from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union

from boa3.internal import constants
from boa3.internal.model.builtin.builtin import Builtin, BoaPackage
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.model.builtin.native.nativecontract import NativeContract
from boa3.internal.model.event import Event
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.imports.package import Package
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.math import Math
from boa3.internal.model.type.typeutils import TypeUtils

__all__ = ['get_package',
           'get_internal_symbol',
           'CompilerBuiltin'
           ]


def get_package(package_full_path: str) -> Optional[Package]:
    return CompilerBuiltin.instance().get_package(package_full_path)


def get_internal_symbol(symbol_id: str) -> Optional[ISymbol]:
    return CompilerBuiltin.instance().get_internal_symbol(symbol_id)


class CompilerBuiltin:
    _instance = None

    @classmethod
    def instance(cls) -> CompilerBuiltin:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.packages: List[Package] = []
        self._events: List[Event] = []

        self._generate_builtin_package('typing', TypeUtils.get_types_from_typing_lib())
        self._generate_builtin_package('math', Math.get_methods_from_math_lib())
        self._generate_builtin_package('boa3.builtin', Builtin.boa_builtins)
        self._set_events(Builtin.builtin_events())
        self._generate_builtin_package('boa3.builtin.contract', Builtin.package_symbols(BoaPackage.Contract))
        self._generate_builtin_package('boa3.builtin.compile_time', Builtin.package_symbols(BoaPackage.CompileTime))
        self._generate_builtin_package('boa3.builtin.interop', Interop.package_symbols)
        self._set_events(Interop.interop_events())
        self._generate_builtin_package('boa3.builtin.nativecontract', NativeContract.package_symbols)
        self._generate_builtin_package('boa3.builtin.type', Builtin.package_symbols(BoaPackage.Type))
        self._generate_builtin_package('boa3.builtin.vm', Builtin.package_symbols(BoaPackage.VM))

    @classmethod
    def reset(cls):
        if cls._instance is not None:
            for event in cls._instance._events:
                event.reset_calls()

    @classmethod
    def update_with_analyser(cls, analyser):
        for pkg in cls.instance().packages:
            if hasattr(pkg, 'update_with_analyser'):
                pkg.update_with_analyser(analyser)

    def _set_events(self, events: List[Event]):
        self._events.extend(events)

    def _generate_builtin_package(self, package_full_path: str,
                                  symbols: Union[Dict[str, ISymbol], List[IdentifiedSymbol]] = None):
        if isinstance(symbols, list):
            symbols = {symbol.identifier: symbol for symbol in symbols}
        if not isinstance(symbols, dict):
            symbols = {}

        package_ids = package_full_path.split(constants.ATTRIBUTE_NAME_SEPARATOR)
        cur_package: Package = None

        for package_id in package_ids:
            package = None

            if isinstance(cur_package, Package):
                if package_id in cur_package.inner_packages:
                    package = cur_package.inner_packages[package_id]
            else:
                package = next((root_package for root_package in self.packages
                                if root_package.identifier == package_id),
                               None)

            if not isinstance(package, Package):
                package = Package(identifier=package_id)
                if isinstance(cur_package, Package):
                    cur_package.include_symbol(package_id, package)
                else:
                    self.packages.append(package)

            cur_package = package

        if isinstance(cur_package, Package):
            for symbol_id, symbol in symbols.items():
                cur_package.include_symbol(symbol_id, symbol)

    def get_package(self, package_full_path: str) -> Optional[Package]:
        package_ids = package_full_path.split(constants.ATTRIBUTE_NAME_SEPARATOR)

        cur_package: Package = next((root_package for root_package in self._instance.packages
                                     if root_package.identifier == package_ids[0]),
                                    None)
        if cur_package is None:
            return None

        for package_id in package_ids[1:]:
            if package_id not in cur_package.inner_packages:
                return None

            cur_package = cur_package.inner_packages[package_id]

        return cur_package

    def get_internal_symbol(self, symbol_id: str) -> Optional[ISymbol]:
        packages_stack: List[Tuple[list, int]] = []
        current_list = self._instance.packages
        current_index = 0

        while len(current_list) > current_index or len(packages_stack) > 0:
            if len(current_list) <= current_index:
                # if didn't find in the current list, go back to the previous list search
                # if the stack is empty, it doesn't continue the loop because the while condition
                current_list, current_index = packages_stack.pop()
                if len(current_list) <= current_index:
                    # if the previous list has no elements unchecked, just continue the loop
                    continue

            package = current_list[current_index]
            if symbol_id in package.symbols and not isinstance(package.symbols[symbol_id], Package):
                return package.symbols[symbol_id]
            current_index += 1

            # if the package has internal packages, searches the symbol in these packages before continuing
            internal_packages = [symbol for symbol in package.inner_packages.values()]
            if len(internal_packages) > 0:
                # save the current list and index in the package
                # made this way to avoid recursive function call
                packages_stack.append((current_list, current_index))
                current_list = internal_packages
                current_index = 0

        if symbol_id in TypeUtils.symbols_for_internal_validation:
            return TypeUtils.symbols_for_internal_validation[symbol_id]
        return None
