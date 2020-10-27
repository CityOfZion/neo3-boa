from boa3.builtin import public


@public
def Main() -> int:
    a = 'just a test'
    return len(a)
