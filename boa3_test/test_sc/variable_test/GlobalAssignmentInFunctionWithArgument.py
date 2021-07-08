from boa3.builtin import public


@public
def Main(a: int) -> int:
    global b
    b = a
    return b


b: int = 0


@public
def get_b() -> int:
    return b
