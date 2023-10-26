import ast
from typing import Dict

from boa3.internal.model.builtin.contract.nep17_interface_methods.nep17interfacemethod import Nep17InterfaceMethod
from boa3.internal.model.builtin.interop.contract import ContractType
from boa3.internal.model.variable import Variable


class Nep17InterfaceTransferMethod(Nep17InterfaceMethod):

    def __init__(self, self_type: ContractType):
        from boa3.internal.model.type.type import Type
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type

        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'from_address': Variable(UInt160Type.build()),
            'to_address': Variable(UInt160Type.build()),
            'amount': Variable(Type.int),
            'data': Variable(Type.any),
        }

        data_default = ast.parse("{0}".format(Type.any.default_value)
                                 ).body[0].value

        super().__init__(args, 'transfer', return_type=Type.bool, defaults=[data_default])
