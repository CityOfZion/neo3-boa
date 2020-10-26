from boa3.builtin import public


@public
def Main(a: bytes) -> int:
    return a[-1]
