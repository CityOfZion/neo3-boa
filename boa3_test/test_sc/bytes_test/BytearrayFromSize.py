from boa3.builtin import public


@public
def create_bytearray(size: int) -> bytearray:
    return bytearray(size)
