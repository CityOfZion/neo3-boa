from boa3.builtin.compile_time import public


@public
def omitted_values() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[::-2]


@public
def omitted_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[:5:-2]


@public
def omitted_end() -> list:
    a = [0, 1, 2, 3, 4, 5, 6]
    return a[2::-2]


@public
def negative_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[-6::-2]


@public
def negative_end() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[:-1:-2]


@public
def negative_really_low_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[-999::-2]


@public
def negative_really_low_end() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[:-999:-2]


@public
def really_high_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[999::-2]


@public
def really_high_end() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[:999:-2]
