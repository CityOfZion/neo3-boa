from typing import Any, List, Tuple

from boa3.builtin.compile_time import public


@public
def copy_list(list_: List[Any], value: Any) -> Tuple[List[Any], List[Any]]:
    list_copy = List.copy(list_)

    list_copy.append(value)

    lists = (list_, list_copy)
    return lists
