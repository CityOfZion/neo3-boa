from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetCandidatesMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'get_candidates'
        native_identifier = 'getCandidates'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args,
                         return_type=Type.list.build_collection([
                             Type.tuple.build_collection([
                                 ECPointType.build(),
                                 Type.int])]))
