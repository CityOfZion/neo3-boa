from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes, to_int


@public
def main(value: int) -> int:
    var = return_int(to_bytes(value))

    return var


def return_int(arg1: bytes) -> int:
    return to_int(arg1)
