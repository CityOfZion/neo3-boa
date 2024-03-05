from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.nativecontract.Nep17.getnep17scripthashmethod import GetNep17ScriptHashMethod


class GetNeoScriptHashMethod(GetNep17ScriptHashMethod):
    def __init__(self):
        from boa3.internal.constants import NEO_SCRIPT
        identifier = '-get_neo'
        super().__init__(NEO_SCRIPT, identifier)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class NeoProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'NEO'
        getter = GetNeoScriptHashMethod()
        super().__init__(identifier, getter)


NeoToken = NeoProperty()
