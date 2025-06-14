from boa3.sc.compiletime import public


@public
def without_attribution_true() -> bool:
    a = 1
    b = 2
    return a is not b


@public
def without_attribution_false() -> bool:
    a = 1
    b = 1
    return a is not b


@public
def with_attribution() -> bool:
    c = 1
    d = c
    return c is not d
