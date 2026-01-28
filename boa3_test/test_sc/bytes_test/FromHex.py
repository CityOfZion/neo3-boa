from boa3.sc.compiletime import public


@public
def main(string: str) -> bytes:
    return bytes.fromhex(string)
