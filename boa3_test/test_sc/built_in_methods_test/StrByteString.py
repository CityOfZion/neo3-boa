from boa3.builtin.compile_time import public


@public
def str_parameter(value: str) -> str:
    a = str(value)
    return a


@public
def bytes_parameter(value: bytes) -> str:
    a = str(value)
    return a


@public
def empty_parameter() -> str:
    a = str()
    return a
