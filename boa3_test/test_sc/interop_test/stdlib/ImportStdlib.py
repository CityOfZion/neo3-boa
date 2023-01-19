from boa3.builtin.compile_time import public
from boa3.builtin.interop import stdlib


@public
def main(value: str, base: int) -> int:
    return stdlib.atoi(value, base)
