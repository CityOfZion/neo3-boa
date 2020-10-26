from boa3.builtin import public

a: int = 10


@public
def Main() -> int:
    return a
