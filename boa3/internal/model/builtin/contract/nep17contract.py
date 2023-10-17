from typing import Dict

from boa3.internal.model.builtin.interop.contract import ContractType

from boa3.internal.model.method import Method


class Nep17ContractClass(ContractType):
    def __init__(self):
        super().__init__()
        
        self._identifier = 'Nep17Contract'
        
        from boa3.internal.model.builtin.contract.nep17_interface_methods import (
            Nep17InterfaceBalanceOfMethod,
            Nep17InterfaceDecimalsMethod,
            Nep17InterfaceSymbolMethod,
            Nep17InterfaceTotalSupplyMethod,
            Nep17InterfaceTransferMethod,
        )

        self._instance_methods: Dict[str, Method] = {
            'balance_of': Nep17InterfaceBalanceOfMethod(self),
            'decimals': Nep17InterfaceDecimalsMethod(self),
            'symbol': Nep17InterfaceSymbolMethod(self),
            'total_supply': Nep17InterfaceTotalSupplyMethod(self),
            'transfer': Nep17InterfaceTransferMethod(self),
        }

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return self._instance_methods.copy()
