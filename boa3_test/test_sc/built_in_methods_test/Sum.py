from boa3.sc.compiletime import public


@public
def main(x: list[int]) -> int:
    return sum(x)
