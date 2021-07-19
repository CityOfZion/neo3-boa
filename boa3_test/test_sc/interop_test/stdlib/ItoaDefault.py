from boa3.builtin import public
from boa3.builtin.interop.stdlib import itoa


@public
def main(value: int) -> str:
    return itoa(value)
