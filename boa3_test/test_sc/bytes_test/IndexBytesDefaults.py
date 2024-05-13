from boa3.sc.compiletime import public


@public
def main(a: bytes, value: bytes) -> int:
    return a.index(value)
