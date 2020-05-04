from typing import Dict

from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.variable import Variable


class Module:
    """
    A class used to represent a Python module

    :ivar variables: a dictionary that maps each variable with its name. Empty by default.
    :ivar methods: a dictionary that maps each method with its name. Empty by default.
    """

    def __init__(self, variables: Dict[str, Variable] = None, methods: Dict[str, Method] = None):
        if variables is None:
            variables = {}
        self.variables = variables

        if methods is None:
            methods = {}
        self.methods = methods

    @property
    def symbols(self) -> Dict[str, IExpression]:
        """
        Gets all the symbols in the module

        :return: a dictionary that maps each symbol in the module with its name
        """
        symbols = {}
        symbols.update(self.variables)
        symbols.update(self.methods)
        return symbols
