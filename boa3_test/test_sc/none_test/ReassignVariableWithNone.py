from boa3.builtin.compile_time import public


@public
def Main():
    a = 2
    b = a * 2
    a = None
