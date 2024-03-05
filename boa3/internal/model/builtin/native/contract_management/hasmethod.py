from boa3.internal.model.builtin.interop.nativecontract import ContractManagementMethod
from boa3.internal.model.variable import Variable


class HasMethod(ContractManagementMethod):

    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.type import Type

        identifier = 'has_method'
        syscall = 'hasMethod'
        args: dict[str, Variable] = {
            'hash': Variable(UInt160Type.build()),
            'method': Variable(Type.str),
            'parameter_count': Variable(Type.int)
        }

        super().__init__(identifier, syscall, args, return_type=Type.bool)
