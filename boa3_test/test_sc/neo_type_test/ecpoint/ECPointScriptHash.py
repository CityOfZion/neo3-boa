from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint


@public
def Main(public_key: ECPoint) -> bytes:
    return public_key.to_script_hash()
