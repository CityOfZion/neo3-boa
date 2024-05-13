from boa3.sc.compiletime import public


@public
def main(a: str, value: str) -> int:
    return a.index(value)
