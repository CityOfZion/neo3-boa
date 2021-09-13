from typing import Union

from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(mem: Union[bytes, str], value: Union[bytes, str]) -> int:
    return StdLib.memory_search(mem, value)
