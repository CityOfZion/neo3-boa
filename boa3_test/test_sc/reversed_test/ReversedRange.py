from boa3.sc.compiletime import public


@public
def main() -> reversed:
    return reversed(range(3))
