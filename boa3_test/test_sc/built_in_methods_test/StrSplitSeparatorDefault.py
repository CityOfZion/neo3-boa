from boa3.sc.compiletime import public


@public
def main(string: str) -> list[str]:
    return string.split()
