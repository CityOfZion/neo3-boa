from boa3.builtin.compile_time import public


@public
def Main(a: bytearray) -> int:
    return a[-1]
