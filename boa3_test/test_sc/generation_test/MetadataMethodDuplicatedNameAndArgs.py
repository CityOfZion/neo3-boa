from boa3.builtin.compile_time import public


@public(name='Add')
def Main(a: int, b: int) -> int:
    return Add(a, b)


@public(name='Add')
def Add(a: int, b: int) -> int:
    return a + b


@public
def Sub(a: int, b: int) -> int:
    return a - b
