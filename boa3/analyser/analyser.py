from __future__ import annotations

import ast
from typing import Dict

from boa3.analyser.astoptimizer import AstOptimizer
from boa3.analyser.constructanalyser import ConstructAnalyser
from boa3.analyser.moduleanalyser import ModuleAnalyser
from boa3.analyser.typeanalyser import TypeAnalyser
from boa3.builtin import NeoMetadata
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class Analyser(object):
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

        import os
        self.path: str = path
        self.filename: str = path if path is None else os.path.realpath(path)

    @staticmethod
    def analyse(path: str, log: bool = False) -> Analyser:
        """
        Analyses the syntax of the Python code

        :param path: the path of the Python file
        :param log: if compiler errors should be logged.
        :return: a boolean value that represents if the analysis was successful
        :rtype: Analyser
        """
        with open(path, 'rb') as source:
            ast_tree = ast.parse(source.read())

        analyser = Analyser(ast_tree, path, log)
        analyser.__pre_execute()

        # fill symbol table
        if not analyser.__analyse_modules():
            return analyser
        # check is the types are correct
        if not analyser.__check_types():
            return analyser

        analyser.__pos_execute()
        analyser.is_analysed = True

        return analyser

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
        return not type_analyser.has_errors

    def __analyse_modules(self) -> bool:
        """
        Validates the symbols and constructs the symbol table of the ast tree

        :return: a boolean value that represents if the analysis was successful
        """
        module_analyser = ModuleAnalyser(self, self.symbol_table, log=self._log)
        self.symbol_table.update(module_analyser.global_symbols)
        self.ast_tree.body.extend(module_analyser.imported_nodes)
        return not module_analyser.has_errors

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
