from boa3.internal.model.builtin.interop.nativecontract import Nep17Method
from boa3.internal.model.variable import Variable


class SymbolMethod(Nep17Method):

    def __init__(self, contract_script_hash: bytes):
        from boa3.internal.model.type.type import Type

        identifier = 'symbol'
        native_identifier = 'symbol'
        args: dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.str, script_hash=contract_script_hash)
