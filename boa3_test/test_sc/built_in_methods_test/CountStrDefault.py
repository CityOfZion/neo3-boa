from boa3.builtin.compile_time import public


@public
def main(string: str, substring: str) -> int:
    return string.count(substring)
