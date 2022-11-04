from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetCryptoLibScriptHashMethod(ContractGetHashMethod):
    def __init__(self):
        from boa3.constants import CRYPTO_SCRIPT
        from boa3.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_crypto_lib_contract'
        args: Dict[str, Variable] = {}
        super().__init__(CRYPTO_SCRIPT, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class CryptoLibContractProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'CryptoLib'
        getter = GetCryptoLibScriptHashMethod()
        super().__init__(identifier, getter)


CryptoLibContract = CryptoLibContractProperty()
