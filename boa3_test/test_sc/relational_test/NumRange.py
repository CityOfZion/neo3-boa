from boa3.builtin.compile_time import public


@public
def Main(a: int, min: int, max: int) -> bool:
    return min <= a <= max
