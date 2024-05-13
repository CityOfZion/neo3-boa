from boa3.sc.compiletime import public


@public
def main(check: bool) -> int:
    if check:
        abort()
    return 123
