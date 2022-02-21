from typing import Any

from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.builtin.type import ByteString


def main(mem1: ByteString, mem2: ByteString, arg: Any) -> int:
    return StdLib.memory_compare(mem1, mem2, arg)
