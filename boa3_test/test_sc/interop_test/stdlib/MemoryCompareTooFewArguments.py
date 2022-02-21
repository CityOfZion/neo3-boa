from boa3.builtin.interop.stdlib import memory_compare
from boa3.builtin.type import ByteString


def main(mem1: ByteString) -> int:
    return memory_compare(mem1)
