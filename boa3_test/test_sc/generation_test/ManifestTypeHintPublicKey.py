from boa3.builtin.compile_time import public
from boa3.builtin.type import PublicKey, ECPoint


@public
def main(arg: bytes) -> PublicKey:
    return PublicKey(ECPoint(arg))
