from typing import Dict

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.variable import Variable


class CreateStandardAccountMethod(InteropMethod):

    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'create_standard_account'
        syscall = 'System.Contract.CreateStandardAccount'
        args: Dict[str, Variable] = {
            'pub_key': Variable(ECPointType.build())
        }
        super().__init__(identifier, syscall, args, return_type=UInt160Type.build())
