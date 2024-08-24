from boa3.sc.compiletime import public


@public
def Main(a: int, min: int, max: int) -> bool:
    return min <= a <= max
