from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint, PublicKey


@public
def main(arg: bytes) -> PublicKey:
    return PublicKey(ECPoint(arg))
