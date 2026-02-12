from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class StrLenMethod(StdLibMethod):

    def __init__(self):
        identifier = 'str_len'
        syscall = 'strLen'
        args: dict[str, Variable] = {
            'string': Variable(Type.str),
        }

        super().__init__(identifier, syscall, args, return_type=Type.int)
