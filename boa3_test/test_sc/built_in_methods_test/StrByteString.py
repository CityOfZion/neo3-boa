from boa3.sc.compiletime import public


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
