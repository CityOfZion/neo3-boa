from boa3.builtin.compile_time import public


@public
def main(check: bool) -> int:
    if check:
        abort()
    return 123
