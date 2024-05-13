from boa3.sc.compiletime import public


@public
def concat(a: str, b: str) -> str:
    return a + b
