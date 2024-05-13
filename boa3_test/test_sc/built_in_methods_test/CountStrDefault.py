from boa3.sc.compiletime import public


@public
def main(string: str, substring: str) -> int:
    return string.count(substring)
