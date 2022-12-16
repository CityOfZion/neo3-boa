from boa3.builtin.compile_time import public


@public
def Main(condition: bool) -> int:
    # the function has a return to each condition
    return 5 if condition else 10
