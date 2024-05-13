from boa3.sc.compiletime import public
from boa3.sc.utils import to_hex_str


@public
def Main(a: bytes) -> str:
    return to_hex_str(a)
