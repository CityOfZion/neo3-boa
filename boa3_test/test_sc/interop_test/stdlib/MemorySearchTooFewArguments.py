from typing import Union

from boa3.builtin.interop.stdlib import memory_search


def main(mem: Union[bytes, str]) -> int:
    return memory_search(mem)
