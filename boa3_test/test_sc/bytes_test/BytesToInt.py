from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_int


@public
def bytes_to_int() -> int:
    return to_int(b'\x01\x02')
