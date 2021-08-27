from typing import Any, Union

from boa3.builtin import public
from boa3.builtin.interop.crypto import NamedCurve
from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.builtin.type import ECPoint


@public
def Main(message: Any, pubkey: ECPoint, signature: Union[bytes, str], curve: NamedCurve) -> bool:
    return CryptoLib.verify_with_ecdsa(message, pubkey, signature, curve)
