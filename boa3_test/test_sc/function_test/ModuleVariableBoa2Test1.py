from boa3.builtin.compile_time import public

WHAT = 5


@public
def main() -> int:

    m = 3 + WHAT

    return m
