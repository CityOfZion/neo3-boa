from boa3.sc.compiletime import public


@public
def Main(a: int, min: int, max: int):
    b: str = min <= a - 2 <= max
