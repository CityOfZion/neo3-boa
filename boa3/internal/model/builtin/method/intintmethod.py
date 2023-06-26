import ast
from typing import Dict

from boa3.internal.model.builtin.method.intmethod import IntMethod
from boa3.internal.model.variable import Variable


class IntIntMethod(IntMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {
            'value': Variable(Type.int),
        }

        value_default = ast.parse("{0}".format(Type.int.default_value)
                                  ).body[0].value

        super().__init__(args, [value_default])

    def generate_internal_opcodes(self, code_generator):
        # it is the identity function, so there is no need of including another opcode
        super().generate_internal_opcodes(code_generator)
