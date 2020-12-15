from boa3.builtin import public


@public
def testing_something(a: bytes) -> bool:
    if a == a:
        return True
    else:
        return False
