from boa3.sc.compiletime import public


@public
def main(value: bytes, base: int) -> int:
    a = int(value, base)
    return a
