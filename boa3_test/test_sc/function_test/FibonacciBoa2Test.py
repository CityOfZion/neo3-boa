from boa3.builtin import public


@public
def main(fibnumber: int) -> int:
    fibresult = fibR(fibnumber)

    return fibresult


def fibR(n: int) -> int:
    if n == 1 or n == 2:
        return 1

    return fibR(n - 1) + fibR(n - 2)
