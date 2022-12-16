from boa3.builtin.compile_time import public


@public
def omitted_values() -> str:
    a = 'unit_test'
    return a[::2]


@public
def omitted_start() -> str:
    a = 'unit_test'
    return a[:5:2]


@public
def omitted_end() -> str:
    a = 'unit_test'
    return a[2::2]


@public
def negative_start() -> str:
    a = 'unit_test'
    return a[-6::2]


@public
def negative_end() -> str:
    a = 'unit_test'
    return a[:-1:2]


@public
def negative_really_low_start() -> str:
    a = 'unit_test'
    return a[-999::2]


@public
def negative_really_low_end() -> str:
    a = 'unit_test'
    return a[:-999:2]


@public
def really_high_start() -> str:
    a = 'unit_test'
    return a[999::2]


@public
def really_high_end() -> str:
    a = 'unit_test'
    return a[:999:2]
