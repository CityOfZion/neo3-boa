from boa3.builtin.compile_time import public


@public
def Main(a: bool, b: bool, c: bool) -> bool:
    return a or b or c
