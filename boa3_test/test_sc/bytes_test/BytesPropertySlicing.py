from boa3.sc.compiletime import public


class Example:
    def __init__(self, bytes_value: bytes):
        self._bytes_value = bytes_value

    @property
    def bytes_prop(self) -> bytes:
        return self._bytes_value


@public
def main(bytes_value: bytes, start: int, end: int) -> bytes:
    obj = Example(bytes_value)
    return obj.bytes_prop[start:end]
