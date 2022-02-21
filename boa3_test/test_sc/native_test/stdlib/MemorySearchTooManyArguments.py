from typing import Any

from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.builtin.type import ByteString


def main(mem: ByteString, value: ByteString, start: int, backward: bool, arg: Any) -> int:
    return StdLib.memory_search(mem, value, start, backward, arg)
