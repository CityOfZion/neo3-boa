from boa3.sc.compiletime import public


@public
def main(a: list[str], value: str) -> int:
    return a.index(value)
