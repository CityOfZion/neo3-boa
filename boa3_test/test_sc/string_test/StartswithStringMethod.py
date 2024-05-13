from boa3.sc.compiletime import public


@public
def main(string: str, substr: str, start: int, end: int) -> bool:
    return string.startswith(substr, start, end)
