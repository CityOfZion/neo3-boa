from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import memory_search
from boa3.builtin.type import ByteString


@public
def main(mem: ByteString, value: ByteString) -> int:
    return memory_search(mem, value)
