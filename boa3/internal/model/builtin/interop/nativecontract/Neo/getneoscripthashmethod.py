from typing import Optional

from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.nativecontract.Nep17.getnep17scripthashmethod import GetNep17ScriptHashMethod


class GetNeoScriptHashMethod(GetNep17ScriptHashMethod):
    def __init__(self):
        from boa3.internal.constants import NEO_SCRIPT
        identifier = '-get_neo_contract'
        super().__init__(NEO_SCRIPT, identifier)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class NeoContractProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'NeoContract'
        getter = GetNeoScriptHashMethod()
        super().__init__(identifier, getter)


NeoContract = NeoContractProperty()
