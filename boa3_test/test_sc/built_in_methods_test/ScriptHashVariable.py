from boa3.sc.compiletime import public
from boa3.sc.utils import to_script_hash


@public
def Main(a: bytes) -> bytes:
    return to_script_hash(a)
