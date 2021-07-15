from typing import Any, Union

from boa3.builtin.interop.binary import memory_search


def main(mem: Union[bytes, str], value: Union[bytes, str], start: int, backward: bool, arg: Any) -> int:
    return memory_search(mem, value, start, backward, arg)
