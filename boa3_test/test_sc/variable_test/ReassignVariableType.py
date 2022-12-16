from boa3.builtin.compile_time import public


@public
def Main() -> int:
    x = '1234'
    y = x
    x = 1234
    return x
