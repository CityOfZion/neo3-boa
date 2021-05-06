from boa3.builtin import public


@public
def pop_test() -> str:
    a = [1, 2, 3, 4, 5]
    b: str = a.pop(2)
    return b
