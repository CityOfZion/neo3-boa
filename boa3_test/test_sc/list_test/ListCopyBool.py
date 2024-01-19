from typing import List

from boa3.builtin.compile_time import public


@public
def copy_bool_list(_list: List[bool], value: bool) -> List[List[bool]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
