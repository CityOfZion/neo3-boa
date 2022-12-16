from boa3.builtin.compile_time import public


@public
def Main() -> str:
    a1 = 2
    a2 = 3
    a = 'unit_test'
    return a[a1:a2]   # expect 'i'
