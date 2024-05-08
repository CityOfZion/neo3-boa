from typing import Any, Self

from boa3.internal.constants import GAS_SCRIPT
from boa3.internal.model.builtin.interop.contract import GasToken
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class GasClass(INativeContractClass):
    """
    A class used to represent GAS native contract
    """

    def __init__(self):
        super().__init__('GAS', GasToken)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.native.nep17_methods import (BalanceOfMethod, DecimalsMethod, SymbolMethod,
                                                                      TotalSupplyMethod, TransferMethod)

        if len(self._class_methods) == 0:
            self._class_methods = {
                'balanceOf': BalanceOfMethod(GAS_SCRIPT),
                'decimals': DecimalsMethod(GAS_SCRIPT),
                'symbol': SymbolMethod(GAS_SCRIPT),
                'totalSupply': TotalSupplyMethod(GAS_SCRIPT),
                'transfer': TransferMethod(GAS_SCRIPT)
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _Gas

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, GasClass)


_Gas = GasClass()
