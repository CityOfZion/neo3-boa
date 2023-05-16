from boa3.builtin.compile_time import public


@public
def literal_values() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[2:5:2]


@public
def negative_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[-6:5:2]


@public
def negative_end() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[0:-1:2]


@public
def negative_values() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[-6:-1:2]


@public
def negative_really_low_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[-999:5:2]


@public
def negative_really_low_end() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[0:-999:2]


@public
def negative_really_low_values() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[-999:-999:2]


@public
def really_high_start() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[999:5:2]


@public
def really_high_end() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[0:999:2]


@public
def really_high_values() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[999:999:2]


@public
def with_variables(x: int, y: int) -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[x:y:2]
