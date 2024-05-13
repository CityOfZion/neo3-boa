from boa3.sc.compiletime import public


class Example:
    bytes_value = b'unit test'


@public
def main(start: int, end: int) -> bytes:
    return Example.bytes_value[start:end]
