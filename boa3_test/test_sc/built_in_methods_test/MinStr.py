from boa3.sc.compiletime import public


@public
def main(val1: str, val2: str) -> str:
    return min(val1, val2)
