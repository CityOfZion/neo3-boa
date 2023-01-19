from boa3.builtin.compile_time import public


@public
def literal_values() -> range:
    a = range(6)
    return a[2:5:-1]


@public
def negative_start() -> range:
    a = range(6)
    return a[-6:5:-1]


@public
def negative_end() -> range:
    a = range(6)
    return a[0:-1:-1]


@public
def negative_values() -> range:
    a = range(6)
    return a[-6:-1:-1]


@public
def negative_really_low_start() -> range:
    a = range(6)
    return a[-999:5:-1]


@public
def negative_really_low_end() -> range:
    a = range(6)
    return a[0:-999:-1]


@public
def negative_really_low_values() -> range:
    a = range(6)
    return a[-999:-999:-1]


@public
def really_high_start() -> range:
    a = range(6)
    return a[999:5:-1]


@public
def really_high_end() -> range:
    a = range(6)
    return a[0:999:-1]


@public
def really_high_values() -> range:
    a = range(6)
    return a[999:999:-1]
