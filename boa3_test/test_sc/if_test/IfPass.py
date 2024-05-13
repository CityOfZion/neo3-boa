from boa3.sc.compiletime import public


@public
def main(condition: bool) -> int:
    a = 0

    if condition:
        pass

    return a
