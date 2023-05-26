import ast
from typing import Dict

from boa3.internal.model.builtin.method.strmethod import StrMethod
from boa3.internal.model.variable import Variable


class StrByteStringMethod(StrMethod):

    def __init__(self):
        from boa3.internal.model.type.primitive.bytestringtype import ByteStringType
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {
            'object': Variable(ByteStringType.build()),
        }
        object_default = ast.parse("'{0}'".format(Type.str.default_value)).body[0].value

        super().__init__(args, [object_default])

    def generate_internal_opcodes(self, code_generator):
        pass
