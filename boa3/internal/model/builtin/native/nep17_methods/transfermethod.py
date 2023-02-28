import ast
from typing import Dict

from boa3.internal.model.builtin.interop.nativecontract import Nep17Method
from boa3.internal.model.variable import Variable


class TransferMethod(Nep17Method):

    def __init__(self, contract_script_hash: bytes):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        identifier = 'transfer'
        native_identifier = 'transfer'
        args: Dict[str, Variable] = {
            'from_address': Variable(UInt160Type.build()),
            'to_address': Variable(UInt160Type.build()),
            'amount': Variable(Type.int),
            'data': Variable(Type.any),
        }

        data_default = ast.parse("{0}".format(Type.any.default_value)
                                 ).body[0].value

        super().__init__(identifier, native_identifier, args, defaults=[data_default],
                         return_type=Type.bool, script_hash=contract_script_hash)
