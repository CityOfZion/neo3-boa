from boa3.sc.compiletime import public


@public
def main() -> bytes:
    m = b'\x01\x02'

    j = getba()

    return m + j


def getba() -> bytes:
    return b'\xaa\xfe'
