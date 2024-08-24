from boa3.sc.compiletime import public


@public
def main(a: list[bool], value: bool) -> int:
    return a.index(value)
