from boa3.internal.model.builtin.interop.nativecontract import Nep17Method
from boa3.internal.model.variable import Variable


class BalanceOfMethod(Nep17Method):

    def __init__(self, contract_script_hash: bytes):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'balanceOf'
        native_identifier = 'balanceOf'
        args: dict[str, Variable] = {'account': Variable(UInt160Type.build())}
        super().__init__(identifier, native_identifier, args, return_type=Type.int, script_hash=contract_script_hash)
