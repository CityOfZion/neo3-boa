from boa3.builtin.interop.stdlib import memory_search
from boa3.builtin.type import ByteString


def main(mem: ByteString) -> int:
    return memory_search(mem)
