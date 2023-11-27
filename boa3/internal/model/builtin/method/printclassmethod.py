from boa3.internal.model.builtin.method.printmethod import PrintMethod
from boa3.internal.model.type.classes.userclass import UserClass
from boa3.internal.model.type.itype import IType


class PrintClassMethod(PrintMethod):

    def __init__(self, arg_value: IType):
        if not isinstance(arg_value, UserClass):
            from boa3.internal.model.type.classes import userclass
            arg_value = userclass._EMPTY_CLASS

        super().__init__(arg_value)
        self._arg_type = arg_value

    def _generate_print_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        code_generator.convert_builtin_method_call(Builtin.StrClass.build(self._arg_type), is_internal=True)
