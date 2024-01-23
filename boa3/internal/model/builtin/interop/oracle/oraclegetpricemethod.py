from boa3.internal.model.builtin.interop.nativecontract import OracleMethod
from boa3.internal.model.variable import Variable


class OracleGetPriceMethod(OracleMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'get_price'
        syscall = 'getPrice'
        args: dict[str, Variable] = {}

        super().__init__(identifier, syscall, args, return_type=Type.int)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None
