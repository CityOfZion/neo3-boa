from boa3.builtin import public


@public
def concat(a: str, b: str) -> str:
    return a + b
