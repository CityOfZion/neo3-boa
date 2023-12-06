from boa3.builtin.compile_time import public


@public
def sort_test() -> list:
    a = [5, 4, 3, 2, 6, 1]
    a.sort(reverse=True)
    return a
