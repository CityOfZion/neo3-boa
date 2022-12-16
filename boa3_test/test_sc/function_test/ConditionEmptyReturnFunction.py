from boa3.builtin.compile_time import public


@public
def Main(a: int):
    if a > 10:
        return

    b = a % 10
