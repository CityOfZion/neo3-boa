import ast
from typing import Dict

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
        # TODO: Include other analysis as they are implemented
        analyser.__check_types()
        analyser.is_analysed = True  # TODO

        return analyser

    def __include_builtins_symbols(self):
        """
        Include the Python builtins in the global symbol table
        """
        for type in Type:
            self.symbol_table[type.name] = type.symbol

    def __check_types(self) -> bool:
        """
        Performs the type checking

        :return: a boolean value that represents if the analysis was successful
        """
        type_analyser = TypeAnalyser(self.ast_tree)
        return not type_analyser.has_errors
