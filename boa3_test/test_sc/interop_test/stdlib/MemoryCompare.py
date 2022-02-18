from boa3.builtin import public
from boa3.builtin.interop.stdlib import memory_compare
from boa3.builtin.type import ByteString


@public
def main(mem1: ByteString, mem2: ByteString) -> int:
    return memory_compare(mem1, mem2)
