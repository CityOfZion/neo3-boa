from boa3.builtin.compile_time import public


@public
def Main() -> int:
    x = (True, 1, 'ok')
    return x[1]

