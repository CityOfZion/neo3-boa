from boa3.builtin.compile_time import public


class Example:
    def __init__(self, bytes_value: bytes):
        self.bytes_value = bytes_value


@public
def main(bytes_value: bytes, start: int, end: int) -> bytes:
    obj = Example(bytes_value)
    return obj.bytes_value[start:end]
