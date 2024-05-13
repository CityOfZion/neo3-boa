from boa3.sc.compiletime import public


@public
def main(x: bytes | str) -> list[int | str]:
    a = 'unit test'
    b = b'unit test'

    return list(x)
