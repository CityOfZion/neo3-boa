from __future__ import annotations

from typing import Any, Dict, Optional

from boa3.constants import GAS_SCRIPT
from boa3.model.method import Method
from boa3.model.property import Property
from boa3.model.type.classes.classarraytype import ClassArrayType
from boa3.model.variable import Variable


class GasClass(ClassArrayType):
    """
    A class used to represent GAS native contract
    """

    def __init__(self):
        super().__init__('GAS')

        self._variables: Dict[str, Variable] = {}
        self._class_methods: Dict[str, Method] = {}
        self._constructor: Optional[Method] = None

    @property
    def instance_variables(self) -> Dict[str, Variable]:
        return self._variables.copy()

    @property
    def class_variables(self) -> Dict[str, Variable]:
        return {}

    @property
    def properties(self) -> Dict[str, Property]:
        return {}

    @property
    def static_methods(self) -> Dict[str, Method]:
        return {}

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.model.builtin.native.nep17_methods import (BalanceOfMethod, DecimalsMethod, SymbolMethod,
                                                             TotalSupplyMethod, TransferMethod)

        if len(self._class_methods) == 0:
            self._class_methods = {
                'balanceOf': BalanceOfMethod(GAS_SCRIPT),
                'decimals': DecimalsMethod(GAS_SCRIPT),
                'symbol': SymbolMethod(GAS_SCRIPT),
                'totalSupply': TotalSupplyMethod(GAS_SCRIPT),
                'transfer': TransferMethod(GAS_SCRIPT)
            }
        return self._class_methods

    @property
    def instance_methods(self) -> Dict[str, Method]:
        return {}

    def constructor_method(self) -> Optional[Method]:
        return self._constructor

    @classmethod
    def build(cls, value: Any = None) -> GasClass:
        if value is None or cls._is_type_of(value):
            return _Gas

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, GasClass)


_Gas = GasClass()
