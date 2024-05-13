from boa3.sc.compiletime import public


@public
def main() -> list[int]:
    a = [1, 2, 3, 4, 5, 6]
    a[:3] = [10]
    return a
