from typing import Union

from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import memory_compare


@public
def main(mem1: Union[str, bytes], mem2: Union[str, bytes]) -> int:
    return memory_compare(mem1, mem2)
