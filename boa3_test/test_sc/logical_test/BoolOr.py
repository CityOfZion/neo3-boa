from boa3.builtin import public


@public
def Main(a: bool, b: bool) -> bool:
    return a or b
