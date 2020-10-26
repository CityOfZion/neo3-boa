from boa3.builtin import public


@public
def Main(a: bool, b: bool, c: bool) -> bool:
    return a or b or c
