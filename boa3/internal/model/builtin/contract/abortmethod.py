from typing import Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class AbortMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'abort'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=Type.none)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.ABORT, b'')]

    @property
    def _args_on_stack(self) -> int:
        return 0

    @property
    def _body(self) -> Optional[str]:
        return None
