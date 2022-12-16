from boa3.builtin.compile_time import public


@public
def testing_something() -> bool:
    a = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    if a == a:
        return True
    else:
        return False
