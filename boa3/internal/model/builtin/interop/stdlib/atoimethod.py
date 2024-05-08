import ast

from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class AtoiMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'atoi'
        syscall = 'atoi'
        args: dict[str, Variable] = {
            'value': Variable(Type.str),
            'base': Variable(Type.int)
        }

        args_default = ast.parse("{0}".format(10)
                                 ).body[0].value

        super().__init__(identifier, syscall, args, defaults=[args_default], return_type=Type.int)
