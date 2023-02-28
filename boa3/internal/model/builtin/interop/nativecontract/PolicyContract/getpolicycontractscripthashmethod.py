from typing import Dict, Optional

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.variable import Variable


class GetPolicyContractScriptHashMethod(ContractGetHashMethod):
    def __init__(self):
        from boa3.internal.constants import POLICY_SCRIPT
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_policy_contract'
        args: Dict[str, Variable] = {}
        super().__init__(POLICY_SCRIPT, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class PolicyContractProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'PolicyContract'
        getter = GetPolicyContractScriptHashMethod()
        super().__init__(identifier, getter)


PolicyContract = PolicyContractProperty()
