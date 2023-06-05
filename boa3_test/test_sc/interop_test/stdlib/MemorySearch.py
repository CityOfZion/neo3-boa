from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import memory_search


@public
def main(mem: Union[str, bytes], value: Union[str, bytes], start: int, backward: bool) -> int:
    return memory_search(mem, value, start, backward)
