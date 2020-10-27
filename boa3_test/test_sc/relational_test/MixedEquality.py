from boa3.builtin import public


@public
def Main(a: int, b: str) -> bool:
    return a == b
