from boa3.builtin import public


@public
def mixed(a: int, b: int, c: int, d: int, e: int) -> int:
    return a + c * (e - (-d)) // b
