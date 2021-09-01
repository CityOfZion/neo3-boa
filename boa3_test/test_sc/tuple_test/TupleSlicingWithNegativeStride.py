from boa3.builtin import public


@public
def literal_values() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[2:5:-1]


@public
def negative_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[-6:5:-1]


@public
def negative_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[0:-1:-1]


@public
def negative_values() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[-6:-1:-1]


@public
def negative_really_low_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[-999:5:-1]


@public
def negative_really_low_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[0:-999:-1]


@public
def negative_really_low_values() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[-999:-999:-1]


@public
def really_high_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[999:5:-1]


@public
def really_high_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[0:999:-1]


@public
def really_high_values() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[999:999:-1]
