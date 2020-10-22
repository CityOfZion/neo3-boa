from boa3.builtin import public


@public
def Main(condition: bool) -> int:
    a = 2 if condition else 3

    return a
