from boa3.builtin.compile_time import public


@public
def main() -> int:

    mylist = [1, 4, 6, 9, 13]

    d2 = add(mylist[0], mylist[2], get_a_value(mylist[1]))

    return d2


def add(a: int, b: int, c: int) -> int:

    result = a + b + c

    return result


def get_a_value(m: int) -> int:

    return m + 4
