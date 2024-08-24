from typing import Any

from boa3.sc.compiletime import public


@public
def copy_list(_list: list[Any], value: Any) -> list[list[Any]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists


@public
def attribution(_list: list[Any], value: Any) -> bool:
    list_not_copy = _list

    list_not_copy.append(value)

    return len(_list) != len(list_not_copy)
