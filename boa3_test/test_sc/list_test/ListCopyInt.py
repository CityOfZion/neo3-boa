from boa3.builtin.compile_time import public


@public
def copy_int_list(_list: list[int], value: int) -> list[list[int]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
