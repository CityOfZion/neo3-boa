import ast
from abc import ABC
from typing import Any, Dict, List

from boa3.internal.model.builtin.builtincallable import IBuiltinCallable
from boa3.internal.model.decorator import IDecorator
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class IBuiltinDecorator(IBuiltinCallable, IDecorator, ABC):
    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(identifier, args, defaults, return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == len(self.args)

    def validate_values(self, *params: Any) -> List[Any]:
        return []
