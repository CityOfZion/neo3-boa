from boa3.builtin import public
from boa3.builtin.interop.binary import itoa


@public
def main(value: int) -> str:
    return itoa(value)
