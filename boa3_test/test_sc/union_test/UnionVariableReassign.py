from typing import Union


def Main():
    a = 2
    b: Union[int, list] = a
    c = [a, b]
    b = c
