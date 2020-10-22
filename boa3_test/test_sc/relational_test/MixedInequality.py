from boa3.builtin import public


@public
def Main(a: str, b: int) -> bool:
    return a != b
