from boa3.builtin.compile_time import public


@public
def omitted_values() -> bytes:
    a = b'unit_test'
    return a[::2]


@public
def omitted_start() -> bytes:
    a = b'unit_test'
    return a[:5:2]


@public
def omitted_end() -> bytes:
    a = b'unit_test'
    return a[2::2]


@public
def negative_start() -> bytes:
    a = b'unit_test'
    return a[-6::2]


@public
def negative_end() -> bytes:
    a = b'unit_test'
    return a[:-1:2]


@public
def negative_really_low_start() -> bytes:
    a = b'unit_test'
    return a[-999::2]


@public
def negative_really_low_end() -> bytes:
    a = b'unit_test'
    return a[:-999:2]


@public
def really_high_start() -> bytes:
    a = b'unit_test'
    return a[999::2]


@public
def really_high_end() -> bytes:
    a = b'unit_test'
    return a[:999:2]
