from boa3.sc.compiletime import public


@public
def testing_something() -> bool:
    a = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    if a == a:
        return True
    else:
        return False
