from boa3.builtin.compile_time import public


@public
def Main(enter: int) -> int:
    x = enter
    while x < 10:
        x += 1
    else:
        return x
