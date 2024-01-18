from typing import List

from boa3.builtin.compile_time import public


@public
def copy_bytes_list(_list: List[bytes], value: bytes) -> List[List[bytes]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
