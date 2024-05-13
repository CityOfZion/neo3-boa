from boa3.sc.compiletime import public


@public
def main(a: list[str], b: str) -> bool:
    return a[0] == b
