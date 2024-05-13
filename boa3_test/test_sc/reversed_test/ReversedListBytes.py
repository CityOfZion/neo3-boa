from boa3.sc.compiletime import public


@public
def main() -> reversed:
    return reversed([b'1', b'2', b'3'])
