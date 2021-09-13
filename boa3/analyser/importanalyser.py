import ast
import importlib.util
import os
from typing import Dict, List, Optional

from boa3 import constants
from boa3.analyser.astanalyser import IAstAnalyser
from boa3.model import imports
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class ImportAnalyser(IAstAnalyser):

    def __init__(self, import_target: str, importer_file: Optional[str] = None,
                 already_imported_modules: List[str] = None, log: bool = False):
        self.can_be_imported: bool = False
        self.is_builtin_import: bool = False
        self.recursive_import: bool = False
        self._import_identifier: str = import_target
        self._imported_files: List[str] = already_imported_modules if already_imported_modules is not None else []

        super().__init__(ast.Module(body=[]), log=log)

        try:
            module_origin: str = importlib.util.find_spec(import_target).origin
        except BaseException:
            return

        path: List[str] = module_origin.split(os.sep)
        self.filename = path[-1]
        self.path: str = module_origin.replace(os.sep, '/')

        self._find_package(module_origin, importer_file)

    def _find_package(self, module_origin: str, origin_file: Optional[str] = None):
        path: List[str] = module_origin.split(os.sep)

        package = imports.builtin.get_package(self._import_identifier)
        if hasattr(package, 'symbols'):
            self.symbols = package.symbols
            self.can_be_imported = True
            self.is_builtin_import = True
            return

        if not('boa3' in path and '/'.join(path[path.index('boa3'):]).startswith('boa3/builtin')):
            # doesn't analyse boa3.builtin packages that aren't included in the imports.builtin as an user module
            # TODO: refactor when importing from user modules is accepted
            import re

            inside_python_folder = any(re.search(r'python(\d\.?)*', folder.lower()) for folder in path)
            updated_tree = None

            if not (inside_python_folder and 'lib' in path):
                # check circular imports to avoid recursions inside the compiler
                if self.path in self._imported_files:
                    self.recursive_import = True
                    return

                # TODO: only user modules and typing lib imports are implemented
                try:
                    from boa3.analyser.analyser import Analyser
                    files = self._imported_files
                    files.append(origin_file)
                    analyser = Analyser.analyse(module_origin, analysed_files=files, log=self._log)

                    # include only imported symbols
                    if analyser.is_analysed:
                        for symbol_id, symbol in analyser.symbol_table.items():
                            if symbol_id not in Type.all_types():
                                symbol.defined_by_entry = False
                                self.symbols[symbol_id] = symbol

                    self.errors.extend(analyser.errors)
                    self.warnings.extend(analyser.warnings)

                    updated_tree = analyser.ast_tree
                    self.can_be_imported = analyser.is_analysed
                except FileNotFoundError:
                    self.can_be_imported = False

                if updated_tree is not None:
                    self._tree = updated_tree

    @property
    def tree(self) -> ast.AST:
        return self._tree

    def export_symbols(self, identifiers: List[str] = None) -> Dict[str, ISymbol]:
        """
        Gets a dictionary that maps each exported symbol with its identifier

        :param identifiers: list of identifiers of the imported symbols
        :return:
        """
        if identifiers is None:
            identifiers = list([name for name, symbol in self.symbols.items() if symbol is not None])
        if not self.can_be_imported or not isinstance(identifiers, (list, str)):
            return {}

        if isinstance(identifiers, str):
            identifiers = [identifiers]

        if constants.IMPORT_WILDCARD in identifiers:
            symbols = self.symbols.copy()
        else:
            symbols = {symbol_id: symbol for symbol_id, symbol in self.symbols.items()
                       if symbol_id in identifiers and symbol is not None}
        return symbols
