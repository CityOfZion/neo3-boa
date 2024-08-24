from boa3.sc.compiletime import public


@public
def main(string: str, sep: str) -> list[str]:
    return string.split(sep)
