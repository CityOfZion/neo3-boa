from boa3.builtin import public


@public
def Main() -> bool:
    return isinstance(123, int)
