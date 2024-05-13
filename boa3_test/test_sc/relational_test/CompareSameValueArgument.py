from boa3.sc.compiletime import public


@public
def testing_something(a: bytes) -> bool:
    if a == a:
        return True
    else:
        return False
