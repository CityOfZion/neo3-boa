from typing import Union

from boa3.builtin import public
from boa3.builtin.interop.binary import memory_compare


@public
def main(mem1: Union[bytes, str], mem2: Union[bytes, str]) -> int:
    return memory_compare(mem1, mem2)
