from boa3.internal.constants import BYTEORDER


class Integer(int):
    def to_byte_array(self, signed: bool = False, min_length: int = 0) -> bytes:
        """
        Converts an integer value to a immutable byte array

        :param signed: Determines whether two's complement is used to represent the integer.
        :param min_length: Minimum output length.
        :return: Return an array of bytes representing an integer.
        """

        bits_per_byte: int = 8
        aux: int = bits_per_byte - 1
        if self < 0:
            signed = True
        if self > 0 and signed:
            aux += 1  # signed numbers uses an additional bit to represent the signal

        byte_length: int = ((self.bit_length() + aux) // bits_per_byte)
        length = max(min_length, byte_length)

        try:
            return int.to_bytes(self, length, BYTEORDER, signed=signed)
        except OverflowError:
            return int.to_bytes(self, 1 + length, BYTEORDER, signed=signed)

    @classmethod
    def from_bytes(cls, bts: bytes, signed: bool = False, byte_size: int = 0) -> int:
        if byte_size > 0:
            bts = bts[:byte_size]
        return int.from_bytes(bts, BYTEORDER, signed=signed)
