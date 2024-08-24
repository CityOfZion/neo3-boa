from boa3.sc.compiletime import public


@public
def mixed() -> bool:
    a: list[int] = [1, 2, 3]
    b: tuple[str, str] = ('unit', 'test')
    return a is b
