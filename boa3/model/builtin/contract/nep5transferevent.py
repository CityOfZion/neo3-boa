from typing import Dict

from boa3.model.builtin.method.builtinevent import IBuiltinEvent
from boa3.model.variable import Variable


class Nep5TransferEvent(IBuiltinEvent):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'Nep5TransferEvent'
        args: Dict[str, Variable] = {
            'from_addr': Variable(Type.bytes),
            'to_addr': Variable(Type.bytes),
            'amount': Variable(Type.int)
        }
        super().__init__(identifier, args)
        self.name = 'transfer'
