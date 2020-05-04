from typing import Dict

from boa3.model.expression import IExpression
from boa3.model.type.type import IType
from boa3.model.variable import Variable


class Method(IExpression):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar locals: a dictionary that maps each local variable with its name. Empty by default.
    :ivar return_type: the return type of the method. None by default.
    """

    def __init__(self, args: Dict[str, Variable] = None, return_type: IType = None):
        if args is None:
            args = {}
        self.args: Dict[str, Variable] = args
        self.return_type: IType = return_type
        self.locals: Dict[str, Variable] = {}

    def include_variable(self, var_id: str, var: Variable):
        """
        Includes a variable into the list of locals

        :param var_id: variable identifier
        :param var: variable to be included
        """
        if var_id not in self.symbols:
            self.locals[var_id] = var

    @property
    def type(self) -> IType:
        return self.return_type

    @property
    def symbols(self) -> Dict[str, Variable]:
        """
        Gets all the symbols in the module

        :return: a dictionary that maps each symbol in the module with its name
        """
        symbols = {}
        symbols.update(self.args)
        symbols.update(self.locals)
        return symbols
