from __future__ import annotations

import abc
import ast
from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class IInternalMethod(IBuiltinMethod, abc.ABC):

    def __init__(self, identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None,
                 vararg: Optional[Tuple[str, Variable]] = None):
        super().__init__(identifier, args, defaults, return_type, vararg)

    @classmethod
    @abc.abstractmethod
    def instance(cls) -> IInternalMethod:
        pass

    @classmethod
    @abc.abstractmethod
    def is_valid_deploy_method(cls, symbol: ISymbol) -> bool:
        return False
