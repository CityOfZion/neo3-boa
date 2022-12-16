from boa3.builtin.compile_time import public


@public
def positional_order() -> int:
    return calc(x1=1, x2=2, x3=3, x4=4)


@public
def out_of_order() -> int:
    return calc(x3=1, x1=2, x4=3, x2=4)


@public
def mixed_in_order() -> int:
    return calc(5, 6, x3=1, x4=2)


@public
def mixed_out_of_order() -> int:
    return calc(5, 6, x4=1, x3=2)


@public
def default_values() -> int:
    return calc(1, x3=3, x4=4)


@public
def only_default_values_and_kwargs() -> int:
    return calc(x4=4, x2=2)


def calc(x1: int = 0, x2: int = 0, x3: int = 0, x4: int = 0) -> int:
    return x1 * 1000 + x2 * 100 + x3 * 10 + x4
