import ast
from typing import Dict, List

from boa3.model import set_internal_call
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.variable import Variable


class LoadScriptMethod(InteropMethod):

    def __init__(self):
        from boa3.model.builtin.interop.contract.callflagstype import CallFlagsType
        from boa3.model.type.type import Type
        from boa3.model.type.primitive.bytestringtype import ByteStringType

        identifier = 'load_script'
        syscall = 'System.Runtime.LoadScript'
        call_flags: CallFlagsType = CallFlagsType.build()

        args: Dict[str, Variable] = {
            'script': Variable(ByteStringType.build()),
            'args': Variable(Type.sequence),
            'call_flags': Variable(call_flags)
        }

        args_default = ast.parse("{0}".format(Type.sequence.default_value)
                                 ).body[0].value
        call_flags_default = set_internal_call(ast.parse("{0}.{1}".format(call_flags.identifier,
                                                                          call_flags.get_value("NONE").name)
                                                         ).body[0].value)

        super().__init__(identifier, syscall, args, defaults=[args_default, call_flags_default], return_type=Type.any)

    @property
    def generation_order(self) -> List[int]:
        indexes = super().generation_order
        context_index = list(self.args).index('args')

        if indexes[-1] != context_index:
            # args must be the first generated argument
            indexes.remove(context_index)
            indexes.insert(0, context_index)

        return indexes
