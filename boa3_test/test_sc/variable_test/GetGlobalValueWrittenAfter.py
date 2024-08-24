from boa3.sc.compiletime import public

a = 0
b = 1
c = 2
d = 3
e = 4
f = 5


@public
def Main() -> list[int]:
    return [a, b, c, d, e, f, g, h]


g = 6
h = 7
