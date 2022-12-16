from boa3.builtin.compile_time import public


@public
def without_attribution_true() -> bool:
    a = 1
    b = 1
    return a is b


@public
def without_attribution_false() -> bool:
    a = 1
    b = 2
    return a is b


@public
def with_attribution() -> bool:
    c = 1
    d = c
    return c is d
