from boa3.sc.compiletime import public

a = 10


@public
def Main() -> int:
    return a


b = 5


@public
def example() -> int:
    return b
