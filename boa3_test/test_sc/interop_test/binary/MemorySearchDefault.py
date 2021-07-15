from boa3.builtin import public
from boa3.builtin.interop.binary import memory_search


@public
def main(mem: bytes, value: bytes) -> int:
    return memory_search(mem, value)
