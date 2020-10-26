from boa3.builtin import public


@public
def Main(a: bytearray) -> int:
    return a[-1]
