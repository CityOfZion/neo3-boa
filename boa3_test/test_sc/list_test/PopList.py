from boa3.builtin import public


@public
def pop_test() -> int:
    a = [1, 2, 3, 4, 5]
    b = a.pop()
    return b
