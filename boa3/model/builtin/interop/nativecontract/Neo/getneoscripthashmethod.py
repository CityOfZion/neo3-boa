from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.nativecontract.Nep17.getnep17scripthashmethod import GetNep17ScriptHashMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode import OpcodeHelper
from boa3.neo.vm.opcode.Opcode import Opcode


class GetNeoScriptHashMethod(GetNep17ScriptHashMethod):
    def __init__(self):
        from boa3.constants import NEO_SCRIPT
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
