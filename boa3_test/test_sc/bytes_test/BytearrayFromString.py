from boa3.sc.compiletime import public


@public
def main(a: str) -> bytearray:
    b: bytearray = bytearray(a)

    return b
