import ast
from typing import Dict, List

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class CallMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.builtin.interop.contract.callflagstype import CallFlagsType
        from boa3.internal.model.type.type import Type
        identifier = 'call_contract'
        syscall = 'System.Contract.Call'

        call_flags = CallFlagsType.build()
        args: Dict[str, Variable] = {
            'script_hash': Variable(UInt160Type.build()),
            'method': Variable(Type.str),
            'args': Variable(Type.sequence),  # TODO: change when *args is implemented #2kq1hzg
            'call_flags': Variable(call_flags)
        }
        args_default = ast.parse("{0}".format(Type.sequence.default_value)
                                 ).body[0].value
        call_flags_default = set_internal_call(ast.parse("{0}.{1}".format(call_flags.identifier,
                                                                          call_flags.default_value.name)
                                                         ).body[0].value)

        super().__init__(identifier, syscall, args, defaults=[args_default, call_flags_default], return_type=Type.any)

    @property
    def generation_order(self) -> List[int]:
        """
        Gets the indexes order that need to be used during code generation.
        If the order for generation is the same as inputted in code, returns reversed(range(0,len_args))

        :return: Index order for code generation
        """
        indexes = super().generation_order
        args_index = list(self.args).index('args')

        if indexes[0] != args_index:
            # context must be the last generated argument
            indexes.remove(args_index)
            indexes.insert(0, args_index)

        return indexes
