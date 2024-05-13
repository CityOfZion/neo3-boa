from boa3.sc.compiletime import public


@public
def main(string: str) -> str:
    return string.lower()
