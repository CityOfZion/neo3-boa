from typing import Any

from boa3.builtin.interop.stdlib import memory_search
from boa3.builtin.type import ByteString


def main(mem: ByteString, value: ByteString, start: int, backward: bool, arg: Any) -> int:
    return memory_search(mem, value, start, backward, arg)
