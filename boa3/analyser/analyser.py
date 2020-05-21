import ast
from typing import Dict

from boa3.analyser.constructanalyser import ConstructAnalyser
from boa3.analyser.moduleanalyser import ModuleAnalyser
from boa3.analyser.typeanalyser import TypeAnalyser
from boa3.model.symbol import ISymbol
from boa3.model.type.type import Type


class Analyser(object):
    """
    This class is responsible for the semantic analysis of the code

    :ivar symbol_table: a dictionary used to store the identifiers
    """

    def __init__(self, ast_tree: ast.AST):
        self.symbol_table: Dict[str, ISymbol] = {}

        self.ast_tree: ast.AST = ast_tree
        self.is_analysed: bool = False

        self.__include_builtins_symbols()

    @staticmethod
    def analyse(path: str):
        """
        Analyses the syntax of the Python code

        :param path: the path of the Python file
        :return: a boolean value that represents if the analysis was successful
        :rtype: Analyser
        """
        with open(path, 'rb') as source:
            ast_tree = ast.parse(source.read())

        analyser = Analyser(ast_tree)
        analyser.__pre_execute()
        # fill symbol table
        if not analyser.__analyse_modules():
            return analyser
        # check is the types are correct
        if not analyser.__check_types():
            return analyser
        analyser.is_analysed = True  # TODO

        return analyser

    def __include_builtins_symbols(self):
        """
        Include the Python builtins in the global symbol table
        """
        self.symbol_table.update(Type.values())

    def __check_types(self) -> bool:
        """
        Performs the type checking

        :return: a boolean value that represents if the analysis was successful
        """
        type_analyser = TypeAnalyser(self.ast_tree, self.symbol_table)
        return not type_analyser.has_errors

    def __analyse_modules(self) -> bool:
        """
        Validates the symbols and constructs the symbol table of the ast tree

        :return: a boolean value that represents if the analysis was successful
        """
        module_analyser = ModuleAnalyser(self.ast_tree, self.symbol_table)
        self.symbol_table.update(module_analyser.global_symbols)
        return not module_analyser.has_errors

    def __pre_execute(self):
        """
        Pre executes the instructions of the ast for optimization
        """
        self.ast_tree = ConstructAnalyser(self.ast_tree).tree
