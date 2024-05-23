from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetRegisterPriceMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'get_register_price'
        native_identifier = 'getRegisterPrice'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
