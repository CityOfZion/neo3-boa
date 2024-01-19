from typing import List

from boa3.builtin.compile_time import public


@public
def copy_str_list(_list: List[str], value: str) -> List[List[str]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
