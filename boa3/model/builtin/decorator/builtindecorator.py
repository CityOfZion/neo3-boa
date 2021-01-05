import ast
from abc import ABC, abstractmethod
from typing import Dict, List

from boa3.model.builtin.builtincallable import IBuiltinCallable
from boa3.model.expression import IExpression
from boa3.model.method import Method
from boa3.model.type.itype import IType
from boa3.model.variable import Variable


class IBuiltinDecorator(IBuiltinCallable, Method, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(identifier, args, defaults, return_type)

    @abstractmethod
    def validate_parameters(self, *params: IExpression) -> bool:
        """
        Verifies if the given parameters are valid to the method

        :param params: arguments of the method
        :return: True if all arguments are valid. False otherwise.
        """
        pass
