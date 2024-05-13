from typing import cast

from boa3.sc.compiletime import public


@public
def main() -> int:

    j = 10

    d = {
        'a': 1,
        'b': 4,
        4: 'blah',
        'm': j,
        'z': [1, 3, 4, 5, 'abcd', j],
        'mcalll': mymethod(1, 4)
    }

    j4: int = d['mcalll']
    return j4 + cast(list[int], d['z'])[3]


def mymethod(a: int, b: int) -> int:

    return a + b
