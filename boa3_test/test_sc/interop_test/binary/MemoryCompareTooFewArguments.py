from typing import Union

from boa3.builtin.interop.binary import memory_compare


def main(mem1: Union[bytes, str]) -> int:
    return memory_compare(mem1)
