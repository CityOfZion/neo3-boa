from boa3.sc.compiletime import public


@public
def main() -> int:
    a = 123
    del a

    return 123
