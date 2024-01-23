from boa3.internal.model.builtin.contract import NeoAccountStateType
from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetAccountStateMethod(NeoContractMethod):

    def __init__(self, neo_account_state: NeoAccountStateType):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'get_account_state'
        native_identifier = 'getAccountState'
        args: dict[str, Variable] = {
            'account': Variable(UInt160Type.build())
        }
        super().__init__(identifier, native_identifier, args, return_type=neo_account_state)
