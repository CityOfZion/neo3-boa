from boa3.sc.compiletime import public


@public
def Main() -> int:
    a = b'\x01\x02\x03'
    b = len(a)
    return b
