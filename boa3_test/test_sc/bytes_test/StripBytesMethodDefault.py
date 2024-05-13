from boa3.sc.compiletime import public


@public
def main(bytes_value: bytes) -> bytes:
    return bytes_value.strip()
