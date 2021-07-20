from boa3.builtin import public


@public
def main(string: str, substring: str) -> int:
    return string.count(substring)
