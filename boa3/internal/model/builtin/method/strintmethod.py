from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable


class StrIntMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        args: dict[str, Variable] = {
            'object': Variable(Type.int),
        }

        super().__init__(args)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.stdlib import ItoaMethod

        code_generator.convert_builtin_method_call(ItoaMethod(internal_call_args=1), is_internal=True)
