from boa3.sc.compiletime import public


@public
def copy_bytes_list(_list: list[bytes], value: bytes) -> list[list[bytes]]:
    list_copy = _list.copy()

    list_copy.append(value)

    lists = [_list, list_copy]
    return lists
