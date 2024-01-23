from boa3.internal.model.builtin.interop.nativecontract import NeoContractMethod
from boa3.internal.model.variable import Variable


class GetGasPerBlockMethod(NeoContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'get_gas_per_block'
        native_identifier = 'getGasPerBlock'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
