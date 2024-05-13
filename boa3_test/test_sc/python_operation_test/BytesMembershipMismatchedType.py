from boa3.sc.compiletime import public


@public
def main(value: str, some_bytes: bytes) -> bool:
    return value not in some_bytes
