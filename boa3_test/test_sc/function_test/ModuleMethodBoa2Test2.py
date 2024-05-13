from boa3.sc.compiletime import public


BLAH = 10 * 300


@public
def main() -> int:

    m = 3

    j = m + BLAH

    return j
