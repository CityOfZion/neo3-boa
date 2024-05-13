from boa3.sc.compiletime import public


@public
def main(string: str, sep: str, maxsplit: int) -> list[str]:
    return string.split(sep, maxsplit)
