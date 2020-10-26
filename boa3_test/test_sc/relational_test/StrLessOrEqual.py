from boa3.builtin import public


@public
def Main(a: str, b: str) -> bool:
    return a <= b
