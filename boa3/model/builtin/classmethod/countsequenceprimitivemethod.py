from typing import Optional

from boa3.model.builtin.classmethod.countsequencemethod import CountSequenceMethod
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.itype import IType


class CountSequencePrimitiveMethod(CountSequenceMethod):

    def __init__(self, sequence_type: Optional[SequenceType] = None, arg_value: Optional[IType] = None):
        if not isinstance(sequence_type, SequenceType):
            from boa3.model.type.type import Type
            sequence_type = Type.sequence.build_collection([Type.str, Type.int, Type.bytes])

        super().__init__(sequence_type, arg_value)
