from typing import Dict

from boa3.model.expression import IExpression
from boa3.model.variable import Variable


class Method(IExpression):
    """
    A class used to represent a function or a class method

    :ivar args: a dictionary that maps each arg with its name. Empty by default.
    :ivar return_type: the return type of the method. None by default.
    """
    def __init__(self, args: Dict[str, Variable] = {}, return_type: type = None):
        self.args: Dict[str, Variable] = args
        self.return_type: type = return_type

    @property
    def type(self) -> type:
        return self.return_type
