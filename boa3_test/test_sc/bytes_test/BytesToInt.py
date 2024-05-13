from boa3.sc.compiletime import public
from boa3.sc.utils import to_int


@public
def bytes_to_int() -> int:
    return to_int(b'\x01\x02')
