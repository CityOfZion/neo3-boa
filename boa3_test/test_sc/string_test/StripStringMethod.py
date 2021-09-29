from boa3.builtin import public


@public
def main(string: str, chars: str) -> str:
    return string.strip(chars)
