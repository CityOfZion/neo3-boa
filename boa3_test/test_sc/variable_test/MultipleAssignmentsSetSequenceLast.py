from boa3.builtin.compile_time import public


@public
def Main():
    a = [1, 2, 3]
    a[2] = c = b = 2
