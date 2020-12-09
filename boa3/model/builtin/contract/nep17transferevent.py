from typing import Dict

from boa3.model.builtin.method.builtinevent import IBuiltinEvent
from boa3.model.variable import Variable


class Nep17TransferEvent(IBuiltinEvent):

    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'Nep17TransferEvent'
        args: Dict[str, Variable] = {
            'from_addr': Variable(Type.bytes),  # TODO: change bytes to hash160 when possible
            'to_addr': Variable(Type.bytes),    # TODO: change bytes to hash160 when possible
            'amount': Variable(Type.int)
        }
        super().__init__(identifier, args)
        self.name = 'transfer'
