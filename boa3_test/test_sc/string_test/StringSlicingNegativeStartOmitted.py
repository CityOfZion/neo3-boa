from boa3.builtin.compile_time import public


@public
def Main() -> str:
    a = 'unit_test'
    return a[:-4]   # expect 'unit_'
