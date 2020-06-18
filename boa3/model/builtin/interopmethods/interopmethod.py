from typing import Dict, Optional, Tuple, List

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class InteropMethod(IBuiltinMethod):

    def __init__(self, identifier: str, sys_call: str, args: Dict[str, Variable] = None, return_type: IType = None):
        self._sys_call: str = sys_call
        super().__init__(identifier, args, return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        if any(not isinstance(param, IExpression) for param in params):
            return False

        args: List[IType] = [arg.type for arg in self.args.values()]
        if len(params) != len(args):
            return False
        return all(args[index].is_type_of(params[index]) for index in range(len(args)))

    @property
    def interop_method_hash(self) -> bytes:
        from boa3.constants import SIZE_OF_INT32
        from boa3.neo import cryptography
        from boa3.neo.vm.type.String import String

        return cryptography.sha256(String(self._sys_call).to_bytes())[:SIZE_OF_INT32]

    @property
    def opcode(self) -> Optional[Tuple[Opcode, bytes]]:
        return Opcode.SYSCALL, self.interop_method_hash

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
