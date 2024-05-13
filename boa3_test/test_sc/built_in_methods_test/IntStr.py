from boa3.sc.compiletime import public


@public
def main(value: str, base: int) -> int:
    a = int(value, base)
    return a
