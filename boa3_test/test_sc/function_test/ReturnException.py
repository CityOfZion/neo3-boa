from boa3.sc.compiletime import public


@public
def main(x: int) -> bytes:
    if x == 1:
        return b'\x01'
    raise Exception("x must be 1")
