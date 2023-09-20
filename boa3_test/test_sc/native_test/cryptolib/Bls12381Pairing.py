from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib



@public
def main(g1: Any, g2: Any) -> Any:
    return CryptoLib.bls12_381_pairing(g1, g2)
