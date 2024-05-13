from boa3.sc.compiletime import public


@public
def main(string: str, chars: str) -> str:
    return string.strip(chars)
