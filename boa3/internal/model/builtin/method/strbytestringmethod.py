import ast

from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable


class StrBytesMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        args: dict[str, Variable] = {
            'object': Variable(Type.union.build([Type.bytes, Type.str])),
        }
        object_default = ast.parse("'{0}'".format(Type.str.default_value)).body[0].value

        super().__init__(args, [object_default])

    def generate_internal_opcodes(self, code_generator):
        pass
