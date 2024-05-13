from boa3.sc.compiletime import public


@public
def copy_str_list(_list: list[str], value: str) -> list[list[str]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
