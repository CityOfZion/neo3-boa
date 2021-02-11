from boa3.builtin import public


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

    value1 = d['fcall']

    if isinstance(value1, int):
        value2 = d['c']

        if isinstance(value2, list):
            value3 = value2[3]

            if isinstance(value3, int):
                return value1 + value3

    return -1


def mymethod(a: int, b: int) -> int:
    return a + b
