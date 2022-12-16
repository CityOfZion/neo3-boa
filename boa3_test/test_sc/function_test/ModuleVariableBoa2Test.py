from boa3.builtin.compile_time import public

CONST = 8
OTHERCONTS = 1232

WHAT = 5


@public
def main() -> int:

    j = CONST

    b = bleh()

    return CONST + OTHERCONTS + WHAT + b + j


def bleh() -> int:
    return 2 + WHAT
