from boa3.builtin.compile_time import public


@public
def omitted_values() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[::-2]


@public
def omitted_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[:5:-2]


@public
def omitted_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[2::-2]


@public
def negative_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[-6::-2]


@public
def negative_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[:-1:-2]


@public
def negative_really_low_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[-999::-2]


@public
def negative_really_low_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[:-999:-2]


@public
def really_high_start() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[999::-2]


@public
def really_high_end() -> tuple:
    a = (0, 1, 2, 3, 4, 5)
    return a[:999:-2]
