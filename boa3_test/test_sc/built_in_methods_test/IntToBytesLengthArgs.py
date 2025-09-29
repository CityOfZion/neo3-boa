from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


@public
def main(int_value: int, length: int) -> bytes:
    return to_bytes(int_value, length)
