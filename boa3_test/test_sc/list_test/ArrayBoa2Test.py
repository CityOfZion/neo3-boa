from boa3.sc.compiletime import public


@public
def main(index: int) -> int:

    j = 3
    arr = [1, j + 3, 3, 4, gethting(), 6, 7, 8, 9]

    m = arr[index]

    return m


def gethting() -> int:
    return 8
