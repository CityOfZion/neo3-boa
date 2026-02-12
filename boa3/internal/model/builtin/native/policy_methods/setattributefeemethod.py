from boa3.internal.model.builtin.interop.nativecontract import PolicyContractMethod
from boa3.internal.model.builtin.interop.policy.transactionattributetypetype import TransactionAttributeTypeType
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable


class SetAttributeFeeMethod(PolicyContractMethod):

    def __init__(self, tx_attribute_type: TransactionAttributeTypeType):
        identifier = 'set_attribute_fee'
        native_identifier = 'setAttributeFee'
        args: dict[str, Variable] = {
            'attribute_type': Variable(tx_attribute_type),
            'value': Variable(Type.int),
        }
        super().__init__(identifier, native_identifier, args, return_type=Type.none)
