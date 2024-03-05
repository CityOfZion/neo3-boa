from boa3.internal.model.builtin.interop.contract.callflagstype import CallFlagsType
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetCallFlagsMethod(InteropMethod):

    def __init__(self, call_flags_type: CallFlagsType):
        identifier = 'get_call_flags'
        syscall = 'System.Contract.GetCallFlags'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=call_flags_type)
