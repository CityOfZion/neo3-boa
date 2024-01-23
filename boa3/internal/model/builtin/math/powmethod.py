from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PowMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'pow'
        args: dict[str, Variable] = {
            'base': Variable(Type.int),
            'exponent': Variable(Type.int),
        }
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def requires_reordering(self) -> bool:
        return True

    def reorder(self, arguments: list):
        # swap base and exponent  positions
        arguments[0], arguments[1] = arguments[1], arguments[0]

    def generate_internal_opcodes(self, code_generator):
        code_generator.insert_opcode(Opcode.POW)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return
