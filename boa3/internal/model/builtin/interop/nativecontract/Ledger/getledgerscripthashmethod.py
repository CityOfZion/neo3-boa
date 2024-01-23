from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.variable import Variable


class GetLedgerScriptHashMethod(ContractGetHashMethod):
    def __init__(self):
        from boa3.internal.constants import LEDGER_SCRIPT
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_ledger_contract'
        args: dict[str, Variable] = {}
        super().__init__(LEDGER_SCRIPT, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class LedgerContractProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'LedgerContract'
        getter = GetLedgerScriptHashMethod()
        super().__init__(identifier, getter)


LedgerContract = LedgerContractProperty()
