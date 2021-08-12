from boa3.builtin import public


@public
def get_test() -> int:
    a = 123
    b = 456
    c = funcao()
    return a + b + c


@public
def funcao() -> int:
    a = 987
    return a
