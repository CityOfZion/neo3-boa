from typing import Union

from boa3.builtin.nativecontract.stdlib import StdLib


def main(mem1: Union[bytes, str]) -> int:
    return StdLib.memory_compare(mem1)
