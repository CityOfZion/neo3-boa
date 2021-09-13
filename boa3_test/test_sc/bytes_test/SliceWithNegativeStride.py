from boa3.builtin import public


@public
def literal_values() -> bytes:
    a = b'unit_test'
    return a[2:5:-1]


@public
def negative_start() -> bytes:
    a = b'unit_test'
    return a[-6:5:-1]


@public
def negative_end() -> bytes:
    a = b'unit_test'
    return a[0:-1:-1]


@public
def negative_values() -> bytes:
    a = b'unit_test'
    return a[-6:-1:-1]


@public
def negative_really_low_start() -> bytes:
    a = b'unit_test'
    return a[-999:5:-1]


@public
def negative_really_low_end() -> bytes:
    a = b'unit_test'
    return a[0:-999:-1]


@public
def negative_really_low_values() -> bytes:
    a = b'unit_test'
    return a[-999:-999:-1]


@public
def really_high_start() -> bytes:
    a = b'unit_test'
    return a[999:5:-1]


@public
def really_high_end() -> bytes:
    a = b'unit_test'
    return a[0:999:-1]


@public
def really_high_values() -> bytes:
    a = b'unit_test'
    return a[999:999:-1]
