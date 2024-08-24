from boa3.sc.compiletime import public


@public
def sort_test() -> list:
    a = [None, "4", 3, 2, 6, True]
    a.sort()
    return a
