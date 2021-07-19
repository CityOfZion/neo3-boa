from boa3.builtin import public
from boa3.builtin.interop.stdlib import atoi


@public
def main(value: str) -> int:
    return atoi(value)
