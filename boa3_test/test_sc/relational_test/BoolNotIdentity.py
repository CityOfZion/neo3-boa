from boa3.builtin.compile_time import public


@public
def without_attribution_true() -> bool:
    a = True
    b = False
    return a is not b


@public
def without_attribution_false() -> bool:
    a = True
    b = True
    return a is not b


@public
def with_attribution() -> bool:
    c = True
    d = c
    return c is not d
