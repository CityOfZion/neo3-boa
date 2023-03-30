from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import Nep17Method
from boa3.internal.model.variable import Variable


class DecimalsMethod(Nep17Method):

    def __init__(self, contract_script_hash: bytes):
        from boa3.internal.model.type.type import Type

        identifier = 'decimals'
        native_identifier = 'decimals'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.int, script_hash=contract_script_hash)
