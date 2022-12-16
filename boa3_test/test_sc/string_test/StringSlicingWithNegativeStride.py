from boa3.builtin.compile_time import public


@public
def literal_values() -> str:
    a = 'unit_test'
    return a[2:5:-1]


@public
def negative_start() -> str:
    a = 'unit_test'
    return a[-6:5:-1]


@public
def negative_end() -> str:
    a = 'unit_test'
    return a[0:-1:-1]


@public
def negative_values() -> str:
    a = 'unit_test'
    return a[-6:-1:-1]


@public
def negative_really_low_start() -> str:
    a = 'unit_test'
    return a[-999:5:-1]


@public
def negative_really_low_end() -> str:
    a = 'unit_test'
    return a[0:-999:-1]


@public
def negative_really_low_values() -> str:
    a = 'unit_test'
    return a[-999:-999:-1]


@public
def really_high_start() -> str:
    a = 'unit_test'
    return a[999:5:-1]


@public
def really_high_end() -> str:
    a = 'unit_test'
    return a[0:999:-1]


@public
def really_high_values() -> str:
    a = 'unit_test'
    return a[999:999:-1]
