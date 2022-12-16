from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import get_random


@public
def main() -> int:
    return get_random()
