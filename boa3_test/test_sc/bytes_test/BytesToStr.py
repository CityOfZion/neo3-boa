from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_str


@public
def bytes_to_str() -> str:
    return to_str(b'abc')
