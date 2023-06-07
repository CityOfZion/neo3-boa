from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(mem: Union[bytes, str], value: Union[bytes, str], start: int) -> int:
    return StdLib.memory_search(mem, value, start)
