from boa3.builtin.compile_time import public


@public
def Main(condition: bool) -> int:
    a: int = 2 if condition else None

    return a
