from boa3.builtin import public


@public
def Main() -> str:
    a = 'unit_test'
    return a[2:5:2]   # expect 'i_'
