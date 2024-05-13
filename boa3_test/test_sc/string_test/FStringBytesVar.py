from boa3.sc.compiletime import public


@public
def main(a: bytes) -> str:
    fstring = f"F-string: {a}"
    return fstring
