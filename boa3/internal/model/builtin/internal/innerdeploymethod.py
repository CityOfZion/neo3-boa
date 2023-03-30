from __future__ import annotations

import ast
from typing import Dict, Optional

from boa3.internal import constants
from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.internal.internalmethod import IInternalMethod
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.method import Method
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.variable import Variable


class InnerDeployMethod(IInternalMethod):

    @classmethod
    def instance(cls) -> InnerDeployMethod:
        return _INNER_DEPLOY_METHOD

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = constants.DEPLOY_METHOD_ID
        args: Dict[str, Variable] = {
            'data': Variable(Type.any),
            'update': Variable(Type.bool)
        }
        super().__init__(identifier, args, return_type=Type.none)

        self.is_public = True
        self._origin_node = set_internal_call(ast.parse(self._body).body[0])

    @property
    def _body(self) -> Optional[str]:
        method_args = [f"{var_id}: {var_type.type.raw_identifier}"
                       for var_id, var_type in self.args.items()
                       ]

        return f"def {self.identifier}({', '.join(method_args)}): return"

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    def copy(self) -> InnerDeployMethod:
        return InnerDeployMethod()

    @classmethod
    def is_valid_deploy_method(cls, symbol: ISymbol) -> bool:
        if isinstance(symbol, InnerDeployMethod):
            return True
        if isinstance(symbol, IBuiltinMethod):
            return False
        if not isinstance(symbol, Method):
            return False
        else:
            if not symbol.is_public:
                return False

            reference_args = list(_INNER_DEPLOY_METHOD.args.values())
            from boa3.internal.model.type.type import Type
            if symbol.return_type is not Type.none:
                return False

            if len(symbol.args) != len(reference_args):
                return False

            for index, arg in enumerate(symbol.args.values()):
                if not reference_args[index].type.is_equal(arg.type):
                    return False

        return True


_INNER_DEPLOY_METHOD = InnerDeployMethod()
