from boa3.sc.compiletime import public


@public
def Main(a: dict[int, str]) -> str:
    return a[0]  # raises runtime error if the dict doesn't contain this key
