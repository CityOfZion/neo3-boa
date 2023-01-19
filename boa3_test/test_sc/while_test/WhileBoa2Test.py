from boa3.builtin.compile_time import public


@public
def Main() -> int:
    """

    :return:
    """
    a = 0
    b = 0

    c = 22

    while a < 7:

        a = a + 1

        if a == 7:
            break

        while c > 20:
            c = c - 5

    return a + b + c  # expect 24
