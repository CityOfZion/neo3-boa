from boa3.internal.model.builtin.method import LenMethod
from boa3.internal.model.builtin.native.nativecontract import NativeContract
from boa3.internal.model.type.itype import IType


class LenStrMethod(LenMethod):

    def __init__(self, arg_value: IType | None = None):
        super().__init__(arg_value)

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_builtin_method_call(NativeContract.StdLib.class_methods['str_len'])
