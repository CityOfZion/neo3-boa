from typing import cast

from boa3.sc.compiletime import public


@public
def main() -> int:
    j = 10

    d = {
        'a': 32,
        'b': 12,
        4: 'blah',
        'm': j,
        'c': [12, 31, 44, 52, 'abcd', j],
        'fcall': mymethod(10, 4)
    }

    value1: int = d['fcall']

    return value1 + cast(list[int], d['c'])[3]


def mymethod(a: int, b: int) -> int:
    return a + b
