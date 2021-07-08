from boa3.builtin import public


@public
def main(check: bool) -> int:
    if check:
        abort()
    return 123
