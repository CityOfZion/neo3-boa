from boa3.internal.model.builtin.interop.nativecontract import PolicyContractMethod
from boa3.internal.model.variable import Variable


class GetExecFeeFactorMethod(PolicyContractMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'get_exec_fee_factor'
        native_identifier = 'getExecFeeFactor'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
