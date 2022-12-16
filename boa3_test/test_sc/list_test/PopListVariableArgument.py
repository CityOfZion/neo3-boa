from boa3.builtin.compile_time import public


@public
def pop_test(x: int) -> int:
    a = [1, 2, 3, 4, 5]
    b = a.pop(x)
    return b
