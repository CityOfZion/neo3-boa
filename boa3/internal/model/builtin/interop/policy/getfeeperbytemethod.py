from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import PolicyContractMethod
from boa3.internal.model.variable import Variable


class GetFeePerByteMethod(PolicyContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'get_fee_per_byte'
        native_identifier = 'getFeePerByte'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
