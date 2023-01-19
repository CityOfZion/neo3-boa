from boa3.builtin.compile_time import public


@public(name='Add')
def Inc(a: int) -> int:
    return Add(a, 1)


@public(name='Add')
def Add(a: int, b: int) -> int:
    return a + b


@public
def Sub(a: int, b: int) -> int:
    return a - b
