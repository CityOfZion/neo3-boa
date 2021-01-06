from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class MaxMethod(IBuiltinMethod):

    def __init__(self):     # TODO: make it so that it can accept the same parameters as Python
        from boa3.model.type.type import Type
        identifier = 'max'
        args: Dict[str, Variable] = {
            'val1': Variable(Type.int),
            'val2': Variable(Type.int),
        }
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.MAX, b'')]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
