from boa3.sc.compiletime import public

a: int


@public
def Main() -> int:
    return a


a = 10
