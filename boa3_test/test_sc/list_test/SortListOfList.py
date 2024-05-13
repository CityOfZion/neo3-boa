from boa3.sc.compiletime import public


@public
def sort_test() -> list:
    a = [[5, 4], [3], [2, 6, 1]]
    a.sort()
    return a
