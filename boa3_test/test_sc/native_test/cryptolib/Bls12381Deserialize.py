from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib


@public
def main(data: bytes) -> Any:
    return CryptoLib.bls12_381_deserialize(data)
