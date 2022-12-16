from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import atoi


@public
def main(value: str) -> int:
    return atoi(value)
