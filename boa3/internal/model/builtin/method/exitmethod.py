from typing import Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ExitMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'exit'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, args, return_type=Type.none)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.ABORT)

    @property
    def _args_on_stack(self) -> int:
        return 0

    @property
    def _body(self) -> Optional[str]:
        return None
