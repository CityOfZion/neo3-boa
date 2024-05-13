from boa3.sc.compiletime import public


@public
def main(a: bytes) -> reversed:
    return reversed(a)
