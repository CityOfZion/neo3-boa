from boa3.builtin.compile_time import public


@public
def main() -> int:
    j = 10

    d = {
        'a': 1,
        'b': 4,
        4: 22,
        'm': j,
    }

    item = 0

    output = 0
    for item in d.values():
        output += item

    d2 = {
        't': 5,
        'r': 6,
        's': 7
    }

    for item in d2.values():
        output += item

    return output


def my_method(a: int, b: int) -> int:
    return a + b
