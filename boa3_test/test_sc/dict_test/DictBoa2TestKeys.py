from boa3.builtin.compile_time import public


@public
def main() -> str:
    j = 10

    d = {
        'a': 1,
        'b': 4,
        'blah': 4,
        'm': j,
        'z': [1, 3, 4, 5, 'abcd', j],
        'mcalll': my_method(1, 4)
    }

    output = ''
    for item in d.keys():
        output += item

    d2 = {
        't': 5,
        'r': 6,
        's': 'a'
    }

    for item in d2.keys():
        output = output + item

    return output


def my_method(a: int, b: int) -> int:
    return a + b
