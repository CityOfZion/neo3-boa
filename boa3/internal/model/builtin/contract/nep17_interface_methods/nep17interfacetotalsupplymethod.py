from typing import Dict

from boa3.internal.model.builtin.contract.nep17_interface_methods.nep17interfacemethod import Nep17InterfaceMethod
from boa3.internal.model.builtin.interop.contract import ContractType
from boa3.internal.model.variable import Variable


class Nep17InterfaceTotalSupplyMethod(Nep17InterfaceMethod):

    def __init__(self, self_type: ContractType):
        from boa3.internal.model.type.type import Type

        args: Dict[str, Variable] = {'self': Variable(self_type)}
        super().__init__(args, 'total_supply', native_identifier='totalSupply', return_type=Type.int)
