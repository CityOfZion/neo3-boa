import ast
from typing import Dict

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class MemorySearchMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'memory_search'
        native_identifier = 'memorySearch'
        byte_string_type = Type.union.build([Type.bytes, Type.str])

        args: Dict[str, Variable] = {
            'mem': Variable(byte_string_type),
            'value': Variable(byte_string_type),
            'start': Variable(Type.int),
            'backward': Variable(Type.bool),
        }

        start_default = set_internal_call(ast.parse("{0}".format(Type.int.default_value)
                                                    ).body[0].value)
        backward_default = set_internal_call(ast.parse("{0}".format(Type.bool.default_value)
                                                       ).body[0].value)

        super().__init__(identifier, native_identifier, args,
                         defaults=[start_default, backward_default],
                         return_type=Type.int)
