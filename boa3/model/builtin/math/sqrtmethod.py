from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class SqrtMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'sqrt'
        args: Dict[str, Variable] = {'val': Variable(Type.int)}
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.SQRT, b'')]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
