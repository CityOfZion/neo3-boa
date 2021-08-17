from typing import Dict

from boa3.model.builtin.interop.nativecontract import GasMethod
from boa3.model.variable import Variable


class BalanceOfMethod(GasMethod):

    def __init__(self):
        from boa3.model.type.type import Type
        from boa3.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'balanceOf'
        native_identifier = 'balanceOf'
        args: Dict[str, Variable] = {'account': Variable(UInt160Type.build())}
        super().__init__(identifier, native_identifier, args, return_type=Type.int)
