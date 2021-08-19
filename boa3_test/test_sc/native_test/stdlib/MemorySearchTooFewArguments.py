from typing import Union

from boa3.builtin.nativecontract.stdlib import StdLib


def main(mem: Union[bytes, str]) -> int:
    return StdLib.memory_search(mem)
