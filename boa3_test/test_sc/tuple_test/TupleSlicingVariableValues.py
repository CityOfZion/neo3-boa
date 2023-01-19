from boa3.builtin.compile_time import public


@public
def Main() -> tuple:
    a1 = 2
    a2 = 3
    a = (0, 1, 2, 3, 4, 5)
    return a[a1:a2]   # expect (2,)
