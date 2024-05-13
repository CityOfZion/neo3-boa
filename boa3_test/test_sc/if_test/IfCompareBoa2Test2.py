from boa3.sc.compiletime import public


@public
def main(a: int, b: int) -> bool:
    if a == b:
        return True
    return False
