from boa3.builtin.compile_time import public


@public
def create_bytearray(size: int) -> bytearray:
    return bytearray(size)
