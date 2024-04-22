from boa3.builtin.compile_time import public


@public
def main(a: list[int], value: int, start: int, end: int) -> int:
    var = return_same(a.index(value, start, end))

    return var


def return_same(arg: int) -> int:
    return arg
