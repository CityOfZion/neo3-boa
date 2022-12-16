from boa3.builtin.compile_time import public


@public
def add_one(a: int) -> int:
    return 1 + a
