from typing import Dict, List, Optional, Tuple

from boa3.model.builtin.builtinproperty import IBuiltinProperty
from boa3.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.model.builtin.interop.nativecontract.Nep17.getnep17scripthashmethod import GetNep17ScriptHashMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class GetGasScriptHashMethod(GetNep17ScriptHashMethod):
    def __init__(self):
        from boa3.constants import GAS_SCRIPT
        identifier = '-get_gas'
        args: Dict[str, Variable] = {}
        super().__init__(GAS_SCRIPT, identifier)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class GasProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'GAS'
        getter = GetGasScriptHashMethod()
        super().__init__(identifier, getter)
