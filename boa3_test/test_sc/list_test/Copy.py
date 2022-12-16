from typing import Any, List

from boa3.builtin.compile_time import public


@public
def copy_list(_list: List[Any], value: Any) -> List[List[Any]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists


@public
def attribution(_list: List[Any], value: Any) -> bool:
    list_not_copy = _list

    list_not_copy.append(value)

    return len(_list) != len(list_not_copy)
