from boa3.sc.compiletime import public


@public
def main(bytes_value: bytes, sub_bytes: bytes) -> bytes:
    return bytes_value.strip(sub_bytes)
