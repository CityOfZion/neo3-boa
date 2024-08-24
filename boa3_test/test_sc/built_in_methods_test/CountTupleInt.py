from boa3.sc.compiletime import public


@public
def main() -> int:
    a = (1, 2, 3, 4, 1, 1, 0)
    return a.count(1)
