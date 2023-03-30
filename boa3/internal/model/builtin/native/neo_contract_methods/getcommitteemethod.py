from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetCommitteeMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'get_committee'
        native_identifier = 'getCommittee'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.list.build([ECPointType.build()]))
