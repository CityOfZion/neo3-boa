from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint
from boa3.sc.utils import to_script_hash


@public
def Main(public_key: ECPoint) -> bytes:
    return to_script_hash(public_key)
