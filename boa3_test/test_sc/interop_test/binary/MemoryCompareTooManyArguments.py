from typing import Any, Union

from boa3.builtin.interop.binary import memory_compare


def main(mem1: Union[bytes, str], mem2: Union[bytes, str], arg: Any) -> int:
    return memory_compare(mem1, mem2, arg)
