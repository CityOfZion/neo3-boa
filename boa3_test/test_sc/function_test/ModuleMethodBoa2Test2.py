from boa3.builtin.compile_time import public


BLAH = 10 * 300


@public
def main() -> int:

    m = 3

    j = m + BLAH

    return j
