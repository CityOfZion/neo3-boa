from boa3.builtin.compile_time import public


@public
def copy_bool_list(_list: list[bool], value: bool) -> list[list[bool]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
