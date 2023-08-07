from boa3.builtin.compile_time import public
from boa3.builtin.contract import to_hex_str


@public
def Main(a: bytes) -> str:
    return to_hex_str(a)
