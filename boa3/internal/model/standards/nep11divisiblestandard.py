from boa3.internal.model.builtin.builtin import Builtin
from boa3.internal.model.builtin.interop.iterator import IteratorType
from boa3.internal.model.standards.neostandard import INeoStandard
from boa3.internal.model.standards.standardmethod import StandardMethod
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.type.type import Type


class Nep11DivisibleStandard(INeoStandard):
    def __init__(self):
        type_uint160 = UInt160Type.build()
        type_iterator = IteratorType.build()
        type_token_id = Type.union.build([Type.str, Type.bytes])

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
                           args={'owner': type_uint160},
                           return_type=Type.int),
            StandardMethod('tokensOf', safe=True,
                           args={'owner': type_uint160},
                           return_type=type_iterator),
            StandardMethod('transfer',
                           args={'to': type_uint160,
                                 'tokenId': type_token_id,
                                 'data': Type.any},
                           return_type=Type.bool,
                           literal_implementation=False),
            # exclusive divisible methods below
            StandardMethod('transfer',
                           args={'from': type_uint160,
                                 'to': type_uint160,
                                 'amount': Type.int,
                                 'tokenId': type_token_id,
                                 'data': Type.any},
                           return_type=Type.bool,
                           literal_implementation=False),
            StandardMethod('ownerOf', safe=True,
                           args={'tokenId': type_token_id},
                           return_type=type_iterator,
                           literal_implementation=False),
            StandardMethod('balanceOf', safe=True,
                           args={'owner': type_uint160,
                                 'tokenId': type_token_id},
                           return_type=Type.int,
                           literal_implementation=False),
        ]

        optionals = [
            StandardMethod('tokens', safe=True,
                           args={},
                           return_type=type_iterator),
            StandardMethod('properties', safe=True,
                           args={
                               'tokenId': type_token_id,
                           },
                           return_type=Type.dict,
                           literal_implementation=False),
        ]

        events = [
            Builtin.Nep11Transfer
        ]

        super().__init__(methods, events, optionals)
