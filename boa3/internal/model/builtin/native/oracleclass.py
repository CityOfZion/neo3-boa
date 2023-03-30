from __future__ import annotations

from typing import Any, Dict

from boa3.internal.model.builtin.interop.nativecontract import OracleContract
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class OracleClass(INativeContractClass):
    """
    A class used to represent Oracle class
    """

    def __init__(self):
        super().__init__('Oracle', OracleContract)

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.oracle.oraclegetpricemethod import OracleGetPriceMethod
        from boa3.internal.model.builtin.interop.oracle.oraclerequestmethod import OracleRequestMethod

        if len(self._class_methods) == 0:
            self._class_methods = {
                'get_price': OracleGetPriceMethod(),
                'request': OracleRequestMethod()
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> OracleClass:
        if value is None or cls._is_type_of(value):
            return _Oracle

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, OracleClass)


_Oracle = OracleClass()
