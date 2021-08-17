from typing import Dict

from boa3.model.builtin.interop.nativecontract import GasMethod
from boa3.model.variable import Variable


class SymbolMethod(GasMethod):

    def __init__(self):
        from boa3.model.type.type import Type

        identifier = 'symbol'
        native_identifier = 'symbol'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.str)
