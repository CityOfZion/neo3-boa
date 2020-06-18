import ast
import importlib.util
import os
from typing import Dict, List

from boa3.analyser.astanalyser import IAstAnalyser
from boa3.model.builtin.builtin import Builtin
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class ImportAnalyser(IAstAnalyser):

    def __init__(self, import_target: str):
        self.can_be_imported: bool = False
        self._import_identifier: str = import_target

        module_origin: str = importlib.util.find_spec(import_target).origin
        path: List[str] = module_origin.split(os.sep)

        super().__init__(ast.Module(body=[]), path[-1])
        if import_target is 'typing':
            self.symbols.update(
                {symbol_id: symbol for symbol_id, symbol in self._get_types_from_typing_lib().items()
                 if symbol_id not in Type.builtin_types()
                 })
            self.can_be_imported = True

        else:
            import re
            inside_python_folder = any(re.search(r'python(\d\.?)*', folder.lower()) for folder in path)

            updated_tree = None
            if not (inside_python_folder and 'lib' in path) or 'boa3' in path:
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

                if ('boa3' in path and 'interop' in path
                        and all(symbol in Builtin.interop_methods() for symbol in self.symbols)):
                    self.symbols = self._get_interop_methods(list(self.symbols.keys()))
                    updated_tree = None

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

    def _get_types_from_typing_lib(self) -> Dict[str, ISymbol]:
        import typing
        from types import FunctionType

        type_symbols: Dict[str, ISymbol] = {}
        all_types: List[str] = typing.__all__

        for t_id in all_types:
            attr = getattr(typing, t_id)
            if not isinstance(attr, FunctionType):
                type_id: str = t_id if t_id in Type.all_types() else t_id.lower()
                if type_id in Type.all_types():
                    type_symbols[t_id] = Type.all_types()[type_id]

        return type_symbols

    def _get_interop_methods(self, methods: List[str]) -> Dict[str, ISymbol]:
        return {method_id: method for method_id, method in Builtin.interop_methods().items() if method_id in methods}
