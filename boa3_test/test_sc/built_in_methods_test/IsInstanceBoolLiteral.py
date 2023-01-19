from boa3.builtin.compile_time import public


@public
def Main() -> bool:
    return isinstance(123, bool)
