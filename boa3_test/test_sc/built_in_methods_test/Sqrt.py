from boa3.builtin import public, sqrt


@public
def main(x: int) -> int:
    return sqrt(x)
