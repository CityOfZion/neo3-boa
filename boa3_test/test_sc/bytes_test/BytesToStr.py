from boa3.builtin import public


@public
def bytes_to_str() -> str:
    return b'abc'.to_str()
