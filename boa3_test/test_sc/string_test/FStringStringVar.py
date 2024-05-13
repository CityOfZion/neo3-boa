from boa3.sc.compiletime import public


@public
def main(a: str) -> str:
    fstring = f"F-string: {a}"
    return fstring
