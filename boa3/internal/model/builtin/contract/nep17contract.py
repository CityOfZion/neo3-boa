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

        nep17_methods: list = [
            Nep17InterfaceBalanceOfMethod,
            Nep17InterfaceDecimalsMethod,
            Nep17InterfaceSymbolMethod,
            Nep17InterfaceTotalSupplyMethod,
            Nep17InterfaceTransferMethod,
        ]

        instance_methods: dict[str, Method] = {}
        for nep17_method in nep17_methods:
            nep17_method_obj = nep17_method(self)
            instance_methods[nep17_method_obj.identifier] = nep17_method_obj

        self._instance_methods: dict[str, Method] = instance_methods

    @property
    def instance_methods(self) -> dict[str, Method]:
        return self._instance_methods.copy()
