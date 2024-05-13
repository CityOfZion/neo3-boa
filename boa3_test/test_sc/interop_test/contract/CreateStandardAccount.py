from boa3.sc.compiletime import public
from boa3.sc.utils import create_standard_account
from boa3.sc.types import ECPoint, UInt160


@public
def main(public_key: bytes) -> UInt160:
    return create_standard_account(ECPoint(public_key))
