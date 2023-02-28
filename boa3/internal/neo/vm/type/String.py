from boa3.internal.constants import ENCODING


class String(str):
    def to_bytes(self, min_length: int = 0) -> bytes:
        """
        Converts an string value to a immutable byte array

        :param min_length: Minimum output length.
        :return: Return an array of bytes representing an string.
        """

        bts = bytes(self, ENCODING)
        return bts.ljust(min_length)

    @classmethod
    def from_bytes(cls, bts: bytes) -> str:
        return bts.decode(ENCODING)
