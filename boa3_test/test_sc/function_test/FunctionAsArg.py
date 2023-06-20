from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_bytes, to_int


@public
def main(value: int) -> int:
    var = return_int(to_bytes(value))

    return var


def return_int(arg1: bytes) -> int:
    return to_int(arg1)
