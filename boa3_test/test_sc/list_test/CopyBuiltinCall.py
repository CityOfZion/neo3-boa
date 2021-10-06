from typing import Any, List, Tuple

from boa3.builtin import public


@public
def copy_list(_list: List[Any], value: Any) -> Tuple[List[Any], List[Any]]:
    list_copy = List.copy(_list)

    list_copy.append(value)

    lists = (_list, list_copy)
    return lists
