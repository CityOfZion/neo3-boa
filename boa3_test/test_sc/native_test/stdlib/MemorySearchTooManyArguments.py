from typing import Any, Union

from boa3.builtin.nativecontract.stdlib import StdLib


def main(mem: Union[bytes, str], value: Union[bytes, str], start: int, backward: bool, arg: Any) -> int:
    return StdLib.memory_search(mem, value, start, backward, arg)
