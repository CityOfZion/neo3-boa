from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.stdlib import memory_search


@public
def main(mem: Union[bytes, str], value: Union[bytes, str], start: int) -> int:
    return memory_search(mem, value, start)
