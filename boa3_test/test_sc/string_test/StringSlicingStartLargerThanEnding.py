from boa3.sc.compiletime import public


@public
def Main() -> str:
    a = 'unit_test'
    return a[3:2]   # expect ''
