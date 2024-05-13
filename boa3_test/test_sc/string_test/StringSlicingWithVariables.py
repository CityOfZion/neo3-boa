from boa3.sc.compiletime import public


@public
def Main(x: int, y: int) -> str:
    return 'unit_test'[x:y]
