from boa3.sc.compiletime import public


@public
def Main():
    a = 1
    b = 2
    c = 3

    d = {a: c, b: a, c: b}
