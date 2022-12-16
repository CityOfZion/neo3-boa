from boa3.builtin.compile_time import public


@public
def Main() -> int:
    a = 'just a test'
    return len(a)
