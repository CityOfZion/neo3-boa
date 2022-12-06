from __future__ import annotations

from typing import Any, Dict

from boa3.model.builtin.interop.nativecontract import CryptoLibContract
from boa3.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.model.method import Method


class CryptoLibClass(INativeContractClass):
    """
    A class used to represent CryptoLib native contract
    """

    def __init__(self):
        super().__init__('CryptoLib', CryptoLibContract.getter)

    @property
    def class_methods(self) -> Dict[str, Method]:
        # avoid recursive import
        from boa3.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'murmur32': Interop.Murmur32,
                'sha256': Interop.Sha256,
                'ripemd160': Interop.Ripemd160,
                'verify_with_ecdsa': Interop.VerifyWithECDsa,
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> CryptoLibClass:
        if value is None or cls._is_type_of(value):
            return _CryptoLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, CryptoLibClass)


_CryptoLib = CryptoLibClass()
