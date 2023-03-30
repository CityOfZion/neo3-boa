import ast
from abc import abstractmethod
from typing import Optional

from boa3.internal.model.expression import IExpression
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol


class IDecorator(Method):

    @abstractmethod
    def validate_parameters(self, *params: IExpression) -> bool:
        """
        Verifies if the given parameters are valid to the method

        :param params: arguments of the method
        :return: True if all arguments are valid. False otherwise.
        """
        pass

    def update_args(self, args: ast.arguments, origin: Optional[ISymbol] = None):
        """
        Updates the given args object if this decorator has any specific cases.
        If this is not the case, DON'T overwrite this method

        :param args: arguments of the method
        :param origin: internal symbol that is
        """
        return

    @property
    def has_cls_or_self(self) -> bool:
        return False

    @property
    def is_function_decorator(self) -> bool:
        return True

    @property
    def is_class_decorator(self) -> bool:
        return False
