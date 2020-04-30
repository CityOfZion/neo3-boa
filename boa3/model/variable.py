from boa3.model.expression import IExpression


class Variable(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """
    def __init__(self, var_type: type):
        self.var_type: type = var_type

    @property
    def type(self) -> type:
        return self.var_type
