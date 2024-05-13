from boa3.sc.compiletime import public

a = b = c = d = 10
c += 5


@public
def get_a() -> int:
    return a


@public
def get_c() -> int:
    return c


@public
def set_a(value: int):
    global a
    a = value


@public
def set_b(value: int):
    global b
    b = value
