from boa3.sc.compiletime import public


@public
def main() -> int:
    return range(10).count(1)
