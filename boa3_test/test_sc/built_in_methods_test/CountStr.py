from boa3.builtin import public


@public
def main(string: str, substring: str, beginning: int, end: int) -> int:
    return string.count(substring, beginning, end)
