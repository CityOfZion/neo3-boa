from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class AbsMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'abs'
        args: Dict[str, Variable] = {'val': Variable(Type.int)}
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.ABS, b'')]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
