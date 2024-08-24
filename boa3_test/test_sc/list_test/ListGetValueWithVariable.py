from boa3.sc.compiletime import public


@public
def main(a: int) -> int:
    return [0, 1, 2, 3, 4, 5][a]
