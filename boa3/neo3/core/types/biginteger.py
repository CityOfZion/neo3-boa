from __future__ import annotations
from decimal import Decimal, localcontext
from typing import Type


class BigInteger(int):
    """
    An implementation to match the C# BigInteger class as used by the NEO reference project.
    """

    @classmethod
    def ZERO(cls: Type[BigInteger]) -> BigInteger:
        """
        Returns:
            An instance initialized to zero.
        """
        return cls(0)

    @classmethod
    def ONE(cls: Type[BigInteger]) -> BigInteger:
        """
        Returns:
            An instance initialized to one.
        """
        return cls(1)

    @classmethod
    def frombytes(cls: Type[BigInteger], bytes: bytes) -> BigInteger:
        """
        Return the BigInteger represented by the given array of bytes.

        The underlying value is always signed and in little endian format.

        Args:
            bytes: Holds the array of bytes to convert. The argument must either support the buffer protocol or
               be an iterable object producing bytes.
        """
        return cls(int.from_bytes(bytes, 'little', signed=True))

    @property
    def sign(self) -> int:
        """
        Gets a number that indicates the sign (negative, positive, or zero) of the current BigInteger object.

        Returns:
            - -1 The value of this object is negative.
            - 0 The value of this object is 0 (zero).
            - 1  The value of this object is positive.
        """
        if self > 0:
            return 1
        elif self == 0:
            return 0
        return -1

    def to_bytearray(self) -> bytearray:
        """
        Return an array of bytes representing the BigInteger.
        """
        if self == 0:
            return bytearray(b'\x00')

        if self < 0:
            highbyte = 0xff
            data = bytearray(self.to_bytes(1 + ((self.bit_length() + 7) // 8), byteorder='little', signed=True))

            msb = len(data) - 1
            for i, b in enumerate(data[::-1]):
                if b != highbyte:
                    msb -= i
                    break

            needExtraByte = (data[msb] & 0x80) != (highbyte & 0x80)
            if needExtraByte:
                return data
            else:
                return data[:-1]

        try:
            return bytearray(self.to_bytes((self.bit_length() + 7) // 8, byteorder='little', signed=True))
        except OverflowError:
            return bytearray(self.to_bytes(1 + ((self.bit_length() + 7) // 8), byteorder='little', signed=True))

    def __abs__(self, *args, **kwargs):
        return BigInteger(super(BigInteger, self).__abs__(*args, **kwargs))

    def __add__(self, *args, **kwargs):
        return BigInteger(super(BigInteger, self).__add__(*args, **kwargs))

    def __mod__(self, *args, **kwargs):
        with localcontext() as ctx:
            ctx.prec = 100
            d1 = Decimal(self)
            d2 = Decimal(args[0])
            res = int(d1 % d2)
        return BigInteger(res)

    def __mul__(self, *args, **kwargs):
        return BigInteger(super(BigInteger, self).__mul__(*args, **kwargs))

    def __neg__(self, *args, **kwargs):
        return BigInteger(super(BigInteger, self).__neg__(*args, **kwargs))

    def __str__(self, *args, **kwargs):
        return super(BigInteger, self).__str__(*args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return BigInteger(super(BigInteger, self).__sub__(*args, **kwargs))

    def __floordiv__(self, *args, **kwargs):
        return BigInteger(super(BigInteger, self).__floordiv__(*args, **kwargs))

    def __truediv__(self, *args, **kwargs):
        if self < 0 or args[0] < 0:
            return BigInteger(super(BigInteger, self).__truediv__(*args, **kwargs))
        else:
            return BigInteger(super(BigInteger, self).__floordiv__(*args, **kwargs))

    def __rshift__(self, *args, **kwargs):
        shift = args[0]
        if shift < 0:
            shift = abs(shift)
            return BigInteger(super(BigInteger, self).__lshift__(shift, **kwargs))
        else:
            return BigInteger(super(BigInteger, self).__rshift__(*args, **kwargs))

    def __lshift__(self, *args, **kwargs):
        shift = args[0]
        if shift < 0:
            shift = abs(shift)
            return BigInteger(super(BigInteger, self).__rshift__(shift, **kwargs))
        else:
            return BigInteger(super(BigInteger, self).__lshift__(*args, **kwargs))
