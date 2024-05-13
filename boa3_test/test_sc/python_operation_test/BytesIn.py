from boa3.sc.compiletime import public


@public
def main(value: bytes, some_bytes: bytes) -> bool:
    return value in some_bytes
