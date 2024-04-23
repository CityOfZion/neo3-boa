from boa3.builtin.compile_time import public


@public
def Main(iterator: list[int]) -> int:
    for value in iterator:
        return value
    else:
        return 5
