def main():
    """
    :return:
    """
    a = None  # this gets coerced to 0

    b = 1

    if a is None:  # this evaluates to true ( which it is )
        b = 2

    c = a + b  # this evaluates to b + 0, so in this case 2

    return c
