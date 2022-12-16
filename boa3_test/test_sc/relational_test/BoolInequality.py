from boa3.builtin.compile_time import public


@public
def Main(a: bool, b: bool) -> bool:
    return a != b
