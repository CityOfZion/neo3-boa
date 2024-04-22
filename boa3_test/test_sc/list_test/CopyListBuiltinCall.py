from typing import Any

from boa3.builtin.compile_time import public


@public
def copy_list(list_: list[Any], value: Any) -> tuple[list[Any], list[Any]]:
    list_copy = list.copy(list_)

    list_copy.append(value)

    lists = (list_, list_copy)
    return lists
