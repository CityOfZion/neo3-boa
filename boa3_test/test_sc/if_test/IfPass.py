from boa3.builtin.compile_time import public


@public
def main(condition: bool) -> int:
    a = 0

    if condition:
        pass

    return a
