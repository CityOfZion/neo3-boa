from typing import Dict, Any, Optional

from boa3.internal.model.builtin.method import IBuiltinMethod
from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StrSequenceMethod(StrMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        if arg_value is None:
            arg_value = Type.sequence

        args: Dict[str, Variable] = {
            'object': Variable(arg_value),
        }

        super().__init__(args)

    def build(self, value: Any) -> IBuiltinMethod:
        if 'object' in self.args and self.args['object'].type is not Type.any:
            return self

        if Type.sequence.is_type_of(value):
            return StrSequenceMethod(value)

        return super().build(value)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop

        code_generator.convert_builtin_method_call(Interop.JsonSerialize, is_internal=True)
