from boa3.sc.compiletime import public


@public
def main(x: list[int], start: int) -> int:
    return sum(x, start)
