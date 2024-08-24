from boa3.sc.compiletime import public


@public
def Main(a: int, b: int) -> bool:
    is_equal = a == b; is_greater = a > b; is_less = a < b
    return not is_equal
