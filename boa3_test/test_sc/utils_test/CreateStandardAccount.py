from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint, UInt160
from boa3.sc.utils import create_standard_account


@public
def main(public_key: bytes) -> UInt160:
    return create_standard_account(ECPoint(public_key))
