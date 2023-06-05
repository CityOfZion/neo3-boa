from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_bool


@public
def bytes_to_bool(args: bytes) -> bool:
    return to_bool(args)
