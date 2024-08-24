from boa3.sc.compiletime import public


@public
def concat() -> str:
    a = '1,2,3'
    b = a[:-2]
    c = '[' + b + ']'
    return c
