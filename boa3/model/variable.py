from typing import Optional

from boa3.model.expression import IExpression
from boa3.model.type.itype import IType


class Variable(IExpression):
    """
    A class used to represent a variable

    :ivar var_type: the type of the variable.
    """

    def __init__(self, var_type: Optional[IType]):
        self.__var_type: Optional[IType] = var_type

    @property
    def shadowing_name(self) -> str:
        return 'variable'

    @property
    def type(self) -> IType:
        return self.__var_type

    def set_type(self, var_type: IType):
        """
        Sets a type for the variable if its type is not defined

        :param var_type:
        """
        if self.__var_type is None:
            self.__var_type = var_type
