import ast
import importlib.util
import os
from typing import Dict, List

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.model import imports
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class ImportAnalyser(IAstAnalyser):

    def __init__(self, import_target: str):
        self.can_be_imported: bool = False
        self.is_builtin_import: bool = False
        self._import_identifier: str = import_target

        try:
            module_origin: str = importlib.util.find_spec(import_target).origin
        except BaseException:
            return

        path: List[str] = module_origin.split(os.sep)
        self.path: str = module_origin.replace(os.sep, '/')

        super().__init__(ast.Module(body=[]), path[-1])
        self._find_package(module_origin)

    def _find_package(self, module_origin: str):
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
                # TODO: only user modules and typing lib imports are implemented
                try:
                    from boa3.analyser.analyser import Analyser
                    analyser = Analyser.analyse(module_origin)

                    # include only imported symbols
                    if analyser.is_analysed:
                        self.symbols.update(
                            {symbol_id: symbol for symbol_id, symbol in analyser.symbol_table.items()
                             if symbol_id not in Type.all_types()
                             })
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

        symbols = {symbol_id: symbol for symbol_id, symbol in self.symbols.items()
                   if symbol_id in identifiers and symbol is not None}
        return symbols
