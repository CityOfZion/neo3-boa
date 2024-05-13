from boa3.sc.compiletime import public


@public
def main(value: bool) -> str:
    a = str(value)
    return a
