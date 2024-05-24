from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetCommitteeAddressMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'get_committee_address'
        native_identifier = 'getCommitteeAddress'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=UInt160Type.build())
