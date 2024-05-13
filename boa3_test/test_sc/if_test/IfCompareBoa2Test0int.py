from boa3.sc.compiletime import public


@public
def main(a: int, b: int) -> int:
    if a > b:
        return 3
    return 2
