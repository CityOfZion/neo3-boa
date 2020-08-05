from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ScriptHashMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'to_script_hash'
        args: Dict[str, Variable] = {'data_bytes': Variable(Type.any)}
        super().__init__(identifier, args, Type.bytes)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, PrimitiveType)

    @property
    def is_supported(self) -> bool:
        # TODO: change when implement variable values conversion to script hash
        return False

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return []

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
