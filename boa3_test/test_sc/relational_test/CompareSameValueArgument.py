from boa3.builtin.compile_time import public


@public
def testing_something(a: bytes) -> bool:
    if a == a:
        return True
    else:
        return False
