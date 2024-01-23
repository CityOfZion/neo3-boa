import ast

from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class ItoaMethod(StdLibMethod):

    def __init__(self, internal_call_args: int = None):
        from boa3.internal.model.type.type import Type
        identifier = 'itoa'
        syscall = 'itoa'
        args: dict[str, Variable] = {
            'value': Variable(Type.int),
            'base': Variable(Type.int)
        }
        args_default = ast.parse("{0}".format(10)).body[0].value

        super().__init__(identifier, syscall, args, defaults=[args_default], return_type=Type.str,
                         internal_call_args=internal_call_args)
