import sys


class Integer(int):
    def to_byte_array(self, signed=False) -> bytes:
        """
        Converts an integer value to a immutable byte array

        :param signed: Determines whether two's complement is used to represent the integer.
        :return: Return an array of bytes representing an integer.
        """
        byte_length = ((self.bit_length() + 7) // 8)

        if self < 0:
            return int.to_bytes(self, 1 + byte_length, sys.byteorder, signed=True)

        try:
            return int.to_bytes(self, byte_length, sys.byteorder, signed=signed)
        except OverflowError:
            return int.to_bytes(self, 1 + byte_length, sys.byteorder, signed=signed)
