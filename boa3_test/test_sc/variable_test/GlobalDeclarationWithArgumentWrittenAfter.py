from boa3.builtin import public

a: int


@public
def Main() -> int:
    return a


a = 10
