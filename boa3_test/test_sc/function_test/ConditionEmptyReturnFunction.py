from boa3.builtin import public


@public
def Main(a: int):
    if a > 10:
        return

    b = a % 10
