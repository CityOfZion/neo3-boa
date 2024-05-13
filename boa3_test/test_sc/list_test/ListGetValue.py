from boa3.sc.compiletime import public


@public
def Main(a: list[int]) -> int:
    return a[0]  # raises runtime error if the list is empty
