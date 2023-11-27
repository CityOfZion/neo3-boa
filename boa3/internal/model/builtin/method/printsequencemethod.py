from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.model.type.itype import IType


class PrintSequenceMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        from boa3.internal.model.type.type import Type

        if not isinstance(arg_value, IType) or not Type.sequence.is_type_of(arg_value):
            arg_value = Type.list

        super().__init__(arg_value)

    def _generate_print_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        code_generator.convert_builtin_method_call(Builtin.StrSequence, is_internal=True)
