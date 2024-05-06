from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import memory_compare


@public
def main(mem1: str | bytes, mem2: str | bytes) -> int:
    return memory_compare(mem1, mem2)
