from boa3.builtin import public
from boa3.builtin.interop.stdlib import itoa


@public
def main(value: int, base: int) -> str:
    return itoa(value, base)
