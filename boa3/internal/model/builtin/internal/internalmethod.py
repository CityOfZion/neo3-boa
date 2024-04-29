import abc
import ast
from typing import Self

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.symbol import ISymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class IInternalMethod(IBuiltinMethod, abc.ABC):

    def __init__(self,
                 identifier: str,
                 args: dict[str, Variable] = None,
                 defaults: list[ast.AST] = None,
                 return_type: IType = None,
                 vararg: tuple[str, Variable] | None = None,
                 deprecated: bool = False
                 ):
        super().__init__(identifier, args, defaults, return_type, vararg, deprecated=deprecated)

    @classmethod
    @abc.abstractmethod
    def instance(cls) -> Self:
        pass

    @classmethod
    @abc.abstractmethod
    def is_valid_deploy_method(cls, symbol: ISymbol) -> bool:
        return False
