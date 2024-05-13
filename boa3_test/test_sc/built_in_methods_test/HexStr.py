from boa3.sc.compiletime import public
from boa3.sc.utils import to_hex_str


@public
def Main() -> str:
    return to_hex_str(b'abcdefghijklmnopqrstuvwxyz0123456789')


@public
def Main2() -> str:
    return to_hex_str(b'123')
