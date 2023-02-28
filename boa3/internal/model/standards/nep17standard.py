from boa3.internal.model.builtin.builtin import Builtin
from boa3.internal.model.standards.neostandard import INeoStandard
from boa3.internal.model.standards.standardmethod import StandardMethod
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.type.type import Type


class Nep17Standard(INeoStandard):
    def __init__(self):
        type_uint160 = UInt160Type.build()

        methods = [
            StandardMethod('symbol', safe=True,
                           args={},
                           return_type=Type.str),
            StandardMethod('decimals', safe=True,
                           args={},
                           return_type=Type.int),
            StandardMethod('totalSupply', safe=True,
                           args={},
                           return_type=Type.int),
            StandardMethod('balanceOf', safe=True,
                           args={'account': type_uint160},
                           return_type=Type.int),
            StandardMethod('transfer',
                           args={'from': type_uint160,
                                 'to': type_uint160,
                                 'amount': Type.int,
                                 'data': Type.any},
                           return_type=Type.bool)
        ]
        events = [
            Builtin.Nep17Transfer
        ]

        super().__init__(methods, events)
