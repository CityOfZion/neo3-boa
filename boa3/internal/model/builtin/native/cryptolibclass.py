from typing import Any, Self

from boa3.internal.model.builtin.interop.nativecontract import CryptoLibContract
from boa3.internal.model.builtin.native import crypto_lib as cl
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

        if len(self._class_methods) == 0:
            self._class_methods = {
                'recover_secp256k1': cl.RecoverSecp256K1Method(),
                'murmur32': cl.Murmur32Method(),
                'sha256': cl.Sha256Method(),
                'ripemd160': cl.Ripemd160Method(),
                'keccak256': cl.Keccak256Method(),
                'verify_with_ecdsa': cl.VerifyWithECDsaMethod(),
                'bls12_381_add': cl.Bls12381AddMethod(),
                'bls12_381_deserialize': cl.Bls12381DeserializeMethod(),
                'bls12_381_equal': cl.Bls12381EqualMethod(),
                'bls12_381_mul': cl.Bls12381MulMethod(),
                'bls12_381_pairing': cl.Bls12381PairingMethod(),
                'bls12_381_serialize': cl.Bls12381SerializeMethod(),
            }
        return super().class_methods

    @property
    def sha256(self):
        return self.class_methods['sha256']

    @property
    def ripemd160(self):
        return self.class_methods['ripemd160']

    @classmethod
    def build(cls, value: Any = None) -> Self:
        if value is None or cls._is_type_of(value):
            return _CryptoLib

    @classmethod
    def _is_type_of(cls, value: Any):
        return isinstance(value, CryptoLibClass)


_CryptoLib = CryptoLibClass()
