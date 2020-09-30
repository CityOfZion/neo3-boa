import ast
from typing import Dict

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class CallMethod(InteropMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'call_contract'
        syscall = 'System.Contract.Call'
        args: Dict[str, Variable] = {
            'script_hash': Variable(Type.bytes),
            'method': Variable(Type.str),
            'args': Variable(Type.sequence)  # TODO: change when *args is implemented
        }
        args_default = ast.parse("{0}".format(Type.sequence.default_value)
                                 ).body[0].value
        super().__init__(identifier, syscall, args, defaults=[args_default], return_type=Type.any)
