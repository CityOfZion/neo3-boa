from boa3.sc.compiletime import public


@public
def main(a: tuple) -> reversed:
    return reversed(a)
