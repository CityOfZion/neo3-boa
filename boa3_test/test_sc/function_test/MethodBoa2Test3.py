from typing import List

from boa3.builtin import public


@public
def main() -> int:

    a = [1, 2, 3, 4, 5]

    a2 = a[1]

    a3 = a[2]

    e = add(1, 2, 3, 4, a2)

    first_item = get_first_item(a)

    return e + first_item


def add(a: int, b: int, c: int, d: int, e: int) -> int:
    """
    :param a:
    :param b:
    :param c:
    :param d:
    :param e:
    :return:
    """
    result = a + b + c + d + e

    return result


def get_first_item(array_item: List[int]) -> int:
    """
    :param array_item:
    :return:
    """
    return array_item[0]
