from boa3.sc.compiletime import public


@public
def create_bytearray(size: int) -> bytearray:
    return bytearray(size)
