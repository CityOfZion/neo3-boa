from boa3.builtin.compile_time import public


@public
def pop_test() -> list:
    a = [1, 2, 3, 4, 5]
    a.pop()
    return a
