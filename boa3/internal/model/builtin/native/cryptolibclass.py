from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibContract
from boa3.internal.model.builtin.native.inativecontractclass import INativeContractClass
from boa3.internal.model.method import Method


class CryptoLibClass(INativeContractClass):
    """
    A class used to represent CryptoLib native contract
    """

    def __init__(self):
        super().__init__('CryptoLib', CryptoLibContract)

    @property
    def class_methods(self) -> dict[str, Method]:
        # avoid recursive import
        from boa3.internal.model.builtin.interop.interop import Interop

        if len(self._class_methods) == 0:
            self._class_methods = {
                'murmur32': Interop.Murmur32,
                'sha256': Interop.Sha256,
                'ripemd160': Interop.Ripemd160,
                'verify_with_ecdsa': Interop.VerifyWithECDsa,
                'bls12_381_add': Interop.Bls12381Add,
                'bls12_381_deserialize': Interop.Bls12381Deserialize,
                'bls12_381_equal': Interop.Bls12381Equal,
                'bls12_381_mul': Interop.Bls12381Mul,
                'bls12_381_pairing': Interop.Bls12381Pairing,
                'bls12_381_serialize': Interop.Bls12381Serialize,
            }
        return super().class_methods

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _CryptoLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, CryptoLibClass)


_CryptoLib = CryptoLibClass()
