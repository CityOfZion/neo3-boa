from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class PrintBoolMethod(PrintMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        arg_value = Type.bool

        super().__init__(arg_value)

    def _generate_print_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop

        code_generator.insert_opcode(Opcode.NZ)
        code_generator.convert_builtin_method_call(Interop.JsonSerialize, is_internal=True)
