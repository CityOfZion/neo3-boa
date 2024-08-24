from boa3.sc.compiletime import public


@public
def Main() -> str:
    a = 'unit_test'
    return a[:]   # expect 'unit_test'
