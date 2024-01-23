from boa3.internal.model.builtin.builtinproperty import IBuiltinProperty
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.variable import Variable


class GetStdLibScriptHashMethod(ContractGetHashMethod):
    def __init__(self):
        from boa3.internal.constants import STD_LIB_SCRIPT
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        identifier = '-get_std_lib_contract'
        args: dict[str, Variable] = {}
        super().__init__(STD_LIB_SCRIPT, identifier, args, return_type=UInt160Type.build())

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class StdLibProperty(IBuiltinProperty):
    def __init__(self):
        identifier = 'StdLib'
        getter = GetStdLibScriptHashMethod()
        super().__init__(identifier, getter)


StdLibContract = StdLibProperty()
