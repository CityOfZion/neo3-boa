from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.cryptolib import CryptoLib
from boa3.builtin.type import ByteString


@public
def main(data: ByteString, seed: int) -> ByteString:
    return CryptoLib.murmur32(data, seed)
