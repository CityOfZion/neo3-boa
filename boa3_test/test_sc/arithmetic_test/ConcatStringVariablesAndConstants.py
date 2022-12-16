from boa3.builtin.compile_time import public


@public
def concat() -> str:
    a = '1,2,3'
    b = a[:-2]
    c = '[' + b + ']'
    return c
