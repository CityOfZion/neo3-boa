from boa3.builtin.compile_time import public


@public
def Main() -> list:
    return [
        add(1, 2, 3),
        add(9),
        add(5, 6),
        add()
    ]


def add(a: int = 0, b: int = 0, c: int = 0) -> int:
    return a + b + c
