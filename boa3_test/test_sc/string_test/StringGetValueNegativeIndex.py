from boa3.sc.compiletime import public


@public
def main(a: str) -> str:
    return a[-1]     # raises runtime error if the list is empty
