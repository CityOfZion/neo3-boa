from boa3.sc.compiletime import public


@public
def main(bytes_value: bytes, sep: str) -> str:
    return bytes_value.hex(sep)


@public
def bytes_dot_hex(bytes_value: bytes, sep: str) -> str:
    return bytes.hex(bytes_value, sep)


@public
def literal_bytes(sep: str) -> str:
    return b'0123456789abcdef'.hex(sep)
