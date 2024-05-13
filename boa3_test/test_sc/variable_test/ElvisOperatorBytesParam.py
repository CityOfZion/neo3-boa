from boa3.sc.compiletime import public


@public
def main(param: bytes) -> bytes:
    other = param or b"some default value"
    return other
