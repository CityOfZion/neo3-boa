from typing import Dict

from boa3.model.builtin.interop.nativecontract import GasMethod
from boa3.model.variable import Variable


class TotalSupplyMethod(GasMethod):

    def __init__(self):
        from boa3.model.type.type import Type

        identifier = 'totalSupply'
        native_identifier = 'totalSupply'
        args: Dict[str, Variable] = {}
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
