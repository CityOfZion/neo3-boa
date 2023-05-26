from boa3.internal.model.builtin.method.printmethod import PrintMethod


class PrintIntMethod(PrintMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        arg_value = Type.int

        super().__init__(arg_value)

    def _generate_print_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.stdlib.itoamethod import ItoaMethod

        itoa_method = ItoaMethod(internal_call_args=1)
        code_generator.convert_builtin_method_call(itoa_method, is_internal=True)
