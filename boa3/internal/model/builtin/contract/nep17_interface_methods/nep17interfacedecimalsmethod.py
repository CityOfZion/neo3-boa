from boa3.internal.model.builtin.contract.nep17_interface_methods.nep17interfacemethod import Nep17InterfaceMethod
from boa3.internal.model.builtin.interop.contract import ContractType
from boa3.internal.model.variable import Variable


class Nep17InterfaceDecimalsMethod(Nep17InterfaceMethod):

    def __init__(self, self_type: ContractType):
        from boa3.internal.model.type.type import Type

        args: dict[str, Variable] = {'self': Variable(self_type)}
        super().__init__(args, 'decimals', return_type=Type.int)
