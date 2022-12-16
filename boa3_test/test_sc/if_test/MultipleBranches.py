from boa3.builtin.compile_time import public


@public
def Main(value: int) -> int:
    if value < 0:
        a = 0
    elif value < 5:
        a = 5
    elif value < 10:
        a = 10
    elif value < 15:
        a = 15
    else:
        a = 20

    return a
