from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class GetNetworkMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'get_network'
        syscall = 'System.Runtime.GetNetwork'
        args: dict[str, Variable] = {}
        super().__init__(identifier, syscall, args, return_type=Type.int)
