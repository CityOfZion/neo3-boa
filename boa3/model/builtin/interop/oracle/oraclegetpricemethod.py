from typing import Dict, Optional

from boa3.model.builtin.interop.nativecontract import OracleMethod
from boa3.model.variable import Variable


class OracleGetPriceMethod(OracleMethod):

    def __init__(self):
        from boa3.model.type.type import Type

        identifier = 'get_price'
        syscall = 'getPrice'
        args: Dict[str, Variable] = {}

        super().__init__(identifier, syscall, args, return_type=Type.int)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None
