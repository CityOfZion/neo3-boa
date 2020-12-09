from boa3.builtin import public

CONST = 8
OTHERCONTS = 1232

WHAT = 5


@public
def main() -> int:
    """
    :return:
    """

    j = CONST

    b = bleh()

    return CONST + OTHERCONTS + WHAT + b + j


def bleh() -> int:
    """
    :return:
    """
    return 2 + WHAT
