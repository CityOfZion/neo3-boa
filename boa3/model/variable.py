from boa3.model.expression import IExpression
from boa3.model.type.type import IType


class Variable(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """

    def __init__(self, var_type: IType):
        self.var_type: IType = var_type

    @property
    def type(self) -> IType:
        return self.var_type
