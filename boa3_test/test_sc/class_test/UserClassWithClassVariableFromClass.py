from boa3.builtin.compile_time import public


class Example:
    val1 = 1
    val2 = 2


@public
def get_val1() -> int:
    return Example.val1


@public
def get_val2() -> int:
    return Example.val2
