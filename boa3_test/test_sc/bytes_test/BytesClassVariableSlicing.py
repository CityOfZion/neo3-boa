from boa3.builtin.compile_time import public


class Example:
    bytes_value = b'unit test'


@public
def main(start: int, end: int) -> bytes:
    return Example.bytes_value[start:end]
