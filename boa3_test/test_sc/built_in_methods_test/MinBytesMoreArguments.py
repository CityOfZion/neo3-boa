from boa3.sc.compiletime import public


@public
def main() -> bytes:
    return min(b'Lorem', b'ipsum', b'dolor', b'sit', b'amet')
