import ast

from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable


class StringSplitMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'string_split'
        syscall = 'stringSplit'
        args: dict[str, Variable] = {
            'string': Variable(Type.str),
            'separator': Variable(Type.str),
            'remove_empty_entries': Variable(Type.bool),
        }

        args_default = ast.parse("{0}".format(False)
                                 ).body[0].value

        super().__init__(identifier, syscall, args, defaults=[args_default], return_type=Type.list.build([Type.str]))


class StringSplitWithoutRemoveEmptyEntriesMethod(StdLibMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'string_split'
        syscall = 'stringSplit'
        args: dict[str, Variable] = {
            'string': Variable(Type.str),
            'separator': Variable(Type.str),
        }

        args_default = ast.parse("{0}".format(False)
                                 ).body[0].value

        super().__init__(identifier, syscall, args, defaults=[args_default], return_type=Type.list.build([Type.str]))
