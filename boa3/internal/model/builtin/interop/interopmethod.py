import ast
from abc import ABC
from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class InteropMethod(IBuiltinMethod, ABC):

    def __init__(self, identifier: str, sys_call: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        self._sys_call: str = sys_call
        super().__init__(identifier, args, defaults, return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        if len(params) != len(args):
            return False
        return all(args[index].is_type_of(params[index]) for index in range(len(args)))

    @property
    def interop_method_hash(self) -> bytes:
        return self._method_hash(self._sys_call)

    def _method_hash(self, method_name: str) -> bytes:
        from boa3.internal.constants import SIZE_OF_INT32
        from boa3.internal.neo import cryptography
        from boa3.internal.neo.vm.type.String import String

        return cryptography.sha256(String(method_name).to_bytes())[:SIZE_OF_INT32]

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.SYSCALL, self.interop_method_hash)]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
