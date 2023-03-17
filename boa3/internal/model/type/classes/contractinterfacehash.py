from typing import Dict, Optional

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.variable import Variable


class ContractInterfaceGetScriptHashMethod(ContractGetHashMethod):
    def __init__(self, identifier: str, contract_script: bytes):
        identifier = f'-get_{identifier}'
        args: Dict[str, Variable] = {}
        super().__init__(contract_script, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class ContractHashProperty(IBuiltinProperty):
    def __init__(self, identifier: str, contract_script: bytes):
        getter = ContractInterfaceGetScriptHashMethod(identifier, contract_script)
        super().__init__(identifier, getter)
