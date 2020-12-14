__all__ = ['UInt160', 'UInt256']

from boa3.neo import to_hex_str


class _UIntBase(bytes):
    def __init__(self, num_bytes: int, data: bytes = None):
        super(_UIntBase, self).__init__()

        if data is None:
            self._data = bytearray(num_bytes)
        else:
            if isinstance(data, bytes):
                # make sure it's mutable for string representation
                self._data = bytearray(data)
            elif isinstance(data, bytearray):
                self._data = data
            else:
                raise TypeError(f"Invalid data type {type(data)}. Expecting bytes or bytearray")

            if len(self._data) != num_bytes:
                raise ValueError(f"Invalid UInt: data length {len(self._data)} != specified num_bytes {num_bytes}")

    def __str__(self) -> str:
        return to_hex_str(self._data)


class UInt160(_UIntBase):
    _BYTE_LEN = 20

    def __init__(self, data: bytes = None):
        super().__init__(num_bytes=self._BYTE_LEN, data=data)


class UInt256(_UIntBase):
    _BYTE_LEN = 32

    def __init__(self, data: bytes = None):
        super().__init__(num_bytes=self._BYTE_LEN, data=data)
