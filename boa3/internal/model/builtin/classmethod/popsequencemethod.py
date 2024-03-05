import ast

from boa3.internal.model.builtin.classmethod.popmethod import PopMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


class PopSequenceMethod(PopMethod):

    def __init__(self, arg_value: IType | None = None):
        from boa3.internal.model.type.type import Type

        if not Type.mutableSequence.is_type_of(arg_value):
            arg_value = Type.mutableSequence

        args: dict[str, Variable] = {
            'self': Variable(arg_value),
            'index': Variable(arg_value.valid_key)
        }

        index_default = ast.parse("-1").body[0].value.operand
        index_default.n = -1

        super().__init__(args, defaults=[index_default], return_type=arg_value.value_type)

    def generate_opcodes(self, code_generator):
        code_generator.fix_negative_index()
        self.generate_internal_opcodes(code_generator)
