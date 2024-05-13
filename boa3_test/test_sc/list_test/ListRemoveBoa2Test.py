from boa3.sc.compiletime import public


@public
def main() -> list[int]:
    m = [16, 2, 3, 4]
    m.pop(1)
    return m
