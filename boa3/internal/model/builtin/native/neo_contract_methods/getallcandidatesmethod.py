from typing import Dict

from boa3.internal.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetAllCandidatesMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType

        identifier = 'get_all_candidates'
        native_identifier = 'getAllCandidates'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args,
                         return_type=IteratorType.build(Type.tuple.build_collection(
                             [ECPointType.build(), Type.int]
                         )))
