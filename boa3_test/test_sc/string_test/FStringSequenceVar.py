from boa3.sc.compiletime import public


@public
def main(a: list) -> str:
    fstring = f"F-string: {a}"
    return fstring
