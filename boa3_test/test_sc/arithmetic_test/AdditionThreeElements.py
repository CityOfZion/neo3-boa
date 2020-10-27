from boa3.builtin import public


@public
def add_four(a: int, b: int) -> int:
    return 4 + b + a
