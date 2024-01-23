from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class CreateMultisigAccountMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.type import Type

        identifier = 'create_multisig_account'
        syscall = 'System.Contract.CreateMultisigAccount'
        args: dict[str, Variable] = {
            'm': Variable(Type.int),
            'pub_keys': Variable(Type.list.build_collection([ECPointType.build()]))
        }
        super().__init__(identifier, syscall, args, return_type=UInt160Type.build())
