from boa3.sc.compiletime import public


@public
def main() -> int:
    return range(1, 5).index(0)
