from boa3.builtin.compile_time import public


@public
def main() -> int:

    a = 1

    b = 2

    c = stuff()  # 6

    d = stuff2()  # 2

    e = stuff8()

    f = blah()  # 9

    h = prevcall()  # 6

    return a + c + d + f + b + h


def stuff() -> int:
    a = 4

    b = 2

    return a + b


def stuff2() -> int:
    a = 8

    j = 10

    return j - a


def prevcall() -> int:
    return stuff()


def stuff8() -> str:
    q = 'hello'

    return q


def blah() -> int:
    return 1 + 8
