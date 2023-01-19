from boa3.builtin.compile_time import public


@public
def omitted_values() -> range:
    a = range(6)
    return a[::-2]


@public
def omitted_start() -> range:
    a = range(6)
    return a[:5:-2]


@public
def omitted_end() -> range:
    a = range(6)
    return a[2::-2]


@public
def negative_start() -> range:
    a = range(6)
    return a[-6::-2]


@public
def negative_end() -> range:
    a = range(6)
    return a[:-1:-2]


@public
def negative_really_low_start() -> range:
    a = range(6)
    return a[-999::-2]


@public
def negative_really_low_end() -> range:
    a = range(6)
    return a[:-999:-2]


@public
def really_high_start() -> range:
    a = range(6)
    return a[999::-2]


@public
def really_high_end() -> range:
    a = range(6)
    return a[:999:-2]
