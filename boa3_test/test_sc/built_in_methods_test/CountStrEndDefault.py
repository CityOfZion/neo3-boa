from boa3.builtin.compile_time import public


@public
def main(string: str, substring: str, start: int) -> int:
    return string.count(substring, start)
