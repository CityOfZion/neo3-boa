from boa3.internal.model.builtin.interop.nativecontract import PolicyContractMethod
from boa3.internal.model.builtin.interop.policy.transactionattributetypetype import TransactionAttributeTypeType
from boa3.internal.model.variable import Variable


class GetAttributeFeeMethod(PolicyContractMethod):

    def __init__(self, tx_attribute_type: TransactionAttributeTypeType):
        from boa3.internal.model.type.type import Type
        identifier = 'get_attribute_fee'
        native_identifier = 'getAttributeFee'
        args: dict[str, Variable] = {
            'attribute_type': Variable(tx_attribute_type)
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
