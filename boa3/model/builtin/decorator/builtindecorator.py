from abc import ABC, abstractmethod
from typing import Dict

from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class IBuiltinDecorator(Method, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None, return_type: IType = None):
        self.identifier = identifier
        super().__init__(args, return_type)

    @abstractmethod
    def validate_parameters(self, *params: IExpression) -> bool:
        """
        Verifies if the given parameters are valid to the method

        :param params: arguments of the method
        :return: True if all arguments are valid. False otherwise.
        """
        pass
