from boa3.builtin.compile_time import public


@public
def without_attribution_true() -> bool:
    a = 'unit'
    b = 'unit'
    return a is b


@public
def without_attribution_false() -> bool:
    a = 'unit'
    b = 'test'
    return a is b


@public
def with_attribution() -> bool:
    c = 'unit'
    d = c
    return c is d
