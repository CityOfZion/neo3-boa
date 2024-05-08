from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.nativecontract.Nep17.getnep17scripthashmethod import GetNep17ScriptHashMethod


class GetGasScriptHashMethod(GetNep17ScriptHashMethod):
    def __init__(self):
        from boa3.internal.constants import GAS_SCRIPT
        identifier = '-get_gas'
        super().__init__(GAS_SCRIPT, identifier)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class GasProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'GAS'
        getter = GetGasScriptHashMethod()
        super().__init__(identifier, getter)


GasToken = GasProperty()
