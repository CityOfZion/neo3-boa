from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import memory_search


@public
def main(mem: str | bytes, value: str | bytes) -> int:
    return memory_search(mem, value)
