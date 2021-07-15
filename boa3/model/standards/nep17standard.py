from boa3.model.builtin.builtin import Builtin
from boa3.model.standards.neostandard import INeoStandard
from boa3.model.standards.standardmethod import StandardMethod
from boa3.model.type.collection.sequence.uint160type import UInt160Type
from boa3.model.type.type import Type


class Nep17Standard(INeoStandard):
    def __init__(self):
        type_uint160 = UInt160Type.build()

        methods = {
            'symbol': StandardMethod(args={},
                                     return_type=Type.str),
            'decimals': StandardMethod(args={},
                                       return_type=Type.int),
            'totalSupply': StandardMethod(args={},
                                          return_type=Type.int),
            'balanceOf': StandardMethod(args={'account': type_uint160},
                                        return_type=Type.int),
            'transfer': StandardMethod(args={'from': type_uint160,
                                             'to': type_uint160,
                                             'amount': Type.int,
                                             'data': Type.any},
                                       return_type=Type.bool)
        }
        events = [
            Builtin.Nep17Transfer
        ]

        super().__init__(methods, events)
