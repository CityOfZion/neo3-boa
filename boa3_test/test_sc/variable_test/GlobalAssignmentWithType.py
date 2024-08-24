from boa3.sc.compiletime import public

a: int = 10


@public
def Main() -> int:
    return a
