from boa3.sc.compiletime import public


@public
def pop_test() -> int:
    a = [1, 2, 3, 4, 5]
    b = a.pop(2)
    return b
