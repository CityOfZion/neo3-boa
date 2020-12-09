from boa3.builtin import public


@public
def main(fibnumber: int) -> int:
    """
        :param fibnumber:
        :return:
        """
    fibresult = fibR(fibnumber)

    return fibresult


def fibR(n: int) -> int:
    """
    :param n:
    :return:
    """
    if n == 1 or n == 2:
        return 1

    return fibR(n - 1) + fibR(n - 2)
