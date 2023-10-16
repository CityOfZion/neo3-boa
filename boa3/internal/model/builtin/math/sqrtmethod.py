from typing import Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class SqrtMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'sqrt'
        args: Dict[str, Variable] = {'val': Variable(Type.int)}
        super().__init__(identifier, args, return_type=Type.int)

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.SQRT)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return
