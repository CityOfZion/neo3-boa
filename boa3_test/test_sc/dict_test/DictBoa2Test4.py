from boa3.builtin import public


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

    j4 = d['mcalll']

    if isinstance(j4, int):
        j5 = d['z']

        if isinstance(j5, list):
            j6 = j5[3]

            if isinstance(j6, int):
                return j4 + j6
    return -1


def mymethod(a: int, b: int) -> int:

    return a + b
