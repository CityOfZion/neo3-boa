from __future__ import annotations

import ast
from typing import Dict, List, Optional

from boa3 import constants
from boa3.analyser.astanalyser import IAstAnalyser
from boa3.analyser.astoptimizer import AstOptimizer
from boa3.analyser.constructanalyser import ConstructAnalyser
from boa3.analyser.moduleanalyser import ModuleAnalyser
from boa3.analyser.supportedstandard.standardanalyser import StandardAnalyser
from boa3.analyser.typeanalyser import TypeAnalyser
from boa3.builtin import NeoMetadata
from boa3.exception.CompilerError import CompilerError
from boa3.exception.CompilerWarning import CompilerWarning
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class Analyser:
    """
    This class is responsible for the semantic analysis of the code

    :ivar symbol_table: a dictionary used to store the identifiers
    """

    def __init__(self, ast_tree: ast.AST, path: str = None, log: bool = False):
        self.symbol_table: Dict[str, ISymbol] = {}

        self.ast_tree: ast.AST = ast_tree
        self.metadata: NeoMetadata = NeoMetadata()
        self.is_analysed: bool = False
        self._log: bool = log

        self.__include_builtins_symbols()
        self._errors = []
        self._warnings = []

        import os
        self.path: str = path
        self.filename: str = path if path is None else os.path.realpath(path)

    @staticmethod
    def analyse(path: str, log: bool = False, analysed_files: Optional[List[str]] = None) -> Analyser:
        """
        Analyses the syntax of the Python code

        :param path: the path of the Python file
        :param log: if compiler errors should be logged.
        :param analysed_files: a list with the paths of the files that were analysed if it's from an import.
                               if it's not triggered by an import, must be None.
        :return: a boolean value that represents if the analysis was successful
        :rtype: Analyser
        """
        with open(path, 'rb') as source:
            ast_tree = ast.parse(source.read())

        analyser = Analyser(ast_tree, path, log)
        analyser.__pre_execute()

        # fill symbol table
        if not analyser.__analyse_modules(analysed_files):
            return analyser
        # check if standards are correctly implemented
        if not analyser.__check_standards():
            return analyser
        # check is the types are correct
        if not analyser.__check_types():
            return analyser

        analyser.__pos_execute()
        analyser.is_analysed = True

        return analyser

    @property
    def errors(self) -> List[CompilerError]:
        return self._errors.copy()

    @property
    def warnings(self) -> List[CompilerWarning]:
        return self._warnings.copy()

    def __include_builtins_symbols(self):
        """
        Include the Python builtins in the global symbol table
        """
        self.symbol_table.update(Type.builtin_types())

    def __check_types(self) -> bool:
        """
        Performs the type checking

        :return: a boolean value that represents if the analysis was successful
        """
        type_analyser = TypeAnalyser(self, self.symbol_table, log=self._log)
        self.__update_logs(type_analyser)
        return not type_analyser.has_errors

    def __analyse_modules(self, analysed_files: Optional[List[str]] = None) -> bool:
        """
        Validates the symbols and constructs the symbol table of the ast tree

        :return: a boolean value that represents if the analysis was successful
        """
        module_analyser = ModuleAnalyser(self, self.symbol_table,
                                         log=self._log,
                                         filename=self.filename,
                                         analysed_files=analysed_files)
        self.symbol_table.update(module_analyser.global_symbols)
        self.ast_tree.body.extend(module_analyser.imported_nodes)
        self.__update_logs(module_analyser)
        return not module_analyser.has_errors

    def __check_standards(self) -> bool:
        """
        Verify if the standards included in the metadata are fully implemented

        :return: a boolean value that represents if the analysis was successful
        """
        standards_analyser = StandardAnalyser(self, self.symbol_table, log=self._log)
        self.__update_logs(standards_analyser)
        return not standards_analyser.has_errors

    def __update_logs(self, analyser: IAstAnalyser):
        self._errors.extend(analyser.errors)
        self._warnings.extend(analyser.warnings)

    def __pre_execute(self):
        """
        Pre executes the instructions of the ast for optimization
        """
        self.ast_tree = ConstructAnalyser(self.ast_tree, log=self._log).tree

    def __pos_execute(self):
        """
        Tries to optimize the ast after validations
        """
        AstOptimizer(self, log=self._log)

    def update_symbol_table(self, symbol_table: Dict[str, ISymbol]):
        for symbol_id, symbol in symbol_table.items():
            if (hasattr(symbol, 'origin')
                    and hasattr(symbol.origin, 'origin')
                    and isinstance(symbol.origin.origin, ast.AST)
                    and len(symbol_id.split(',')) <= 1):

                if symbol_id in self.symbol_table:
                    self.symbol_table.pop(symbol_id)

                origin_hash = symbol.origin.origin.__hash__()
                unique_id = '{0}{2}{1}'.format(origin_hash, symbol_id, constants.VARIABLE_NAME_SEPARATOR)
            else:
                unique_id = symbol_id

            from boa3.model.identifiedsymbol import IdentifiedSymbol
            if not isinstance(symbol, IdentifiedSymbol):
                if unique_id not in self.symbol_table:
                    self.symbol_table[unique_id] = symbol
