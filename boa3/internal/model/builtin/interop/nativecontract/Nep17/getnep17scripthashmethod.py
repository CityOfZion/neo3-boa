from typing import Dict, Optional

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.variable import Variable


class GetNep17ScriptHashMethod(ContractGetHashMethod):
    def __init__(self, script_hash: bytes, identifier: str = None):
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_nep17_contract' if not isinstance(identifier, str) else identifier
        args: Dict[str, Variable] = {}
        super().__init__(script_hash, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class Nep17ContractProperty(IBuiltinProperty):
    def __init__(self, script_hash: bytes):
        identifier = 'Nep17'
        getter = GetNep17ScriptHashMethod(script_hash)
        super().__init__(identifier, getter)


Nep17Contract = Nep17ContractProperty(b'')
