from boa3.builtin.compile_time import public


@public
def with_attribution() -> bool:
    a: tuple[int, int, int] = (1, 2, 3)
    b = a
    return a is not b


@public
def without_attribution() -> bool:
    a: tuple[int, int, int] = (1, 2, 3)
    b: tuple[int, int, int] = (1, 2, 3)
    return a is not b
