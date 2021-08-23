from typing import Any, Union

from boa3.builtin.nativecontract.stdlib import StdLib


def main(mem1: Union[bytes, str], mem2: Union[bytes, str], arg: Any) -> int:
    return StdLib.memory_compare(mem1, mem2, arg)
