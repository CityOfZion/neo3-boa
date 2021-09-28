from boa3.builtin import public


@public
def main(string: str, substr: str) -> bool:
    return string.startswith(substr)
