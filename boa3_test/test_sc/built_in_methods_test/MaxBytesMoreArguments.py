from boa3.sc.compiletime import public


@public
def main() -> bytes:
    return max(b'Lorem', b'ipsum', b'dolor', b'sit', b'amet')
