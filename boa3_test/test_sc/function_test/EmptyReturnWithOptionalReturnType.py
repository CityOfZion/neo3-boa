from boa3.builtin.compile_time import public


@public
def Main(a: int) -> int | None:
    if a % 2 == 1:
        return  # in this case returns None because the method is not void
    return a // 2
