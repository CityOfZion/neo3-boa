import mmh3  # type: ignore
from bitarray import bitarray  # type: ignore


class BloomFilter:
    """
    BloomFilter implementation conforming to NEO's `implementation <https://github.com/neo-project/neo/blob/982e69090f27c1415872536ce39aea22f0873467/neo.UnitTests/Cryptography/UT_BloomFilter.cs>`_.  # noqa
    """

    def __init__(self, m: int, k: int, ntweak: int, elements: bytearray = None):
        """

        Args:
            m: size of bitarray.
            k: number of hash functions.
            ntweak: correction factor.
            elements: hex-escaped bytearray of values to create the bitarray from.
                Warning: the bit array is truncated to size `m`.

        """
        self.K = k
        self.seeds = [(p * 0xFBA4C795 + ntweak) % 4294967296 for p in range(0, k)]
        if elements:
            tmp_bits = bitarray(endian='little')
            tmp_bits.frombytes(elements)
            # truncate to m bits
            self.bits = tmp_bits[:m]
        else:
            self.bits = bitarray(m, endian='little')
            self.bits.setall(False)
        self.tweak = ntweak

    def add(self, element: bytearray) -> None:
        """
        Add an element to the filter.

        Args:
            element: hex-escaped bytearray.
        """
        for s in self.seeds:
            h = mmh3.hash(element, s, signed=False)
            self.bits[h % self.bits.length()] = True

    def check(self, element: bytearray) -> bool:
        """
        Check if the element is present

        Args:
            element: hex-escaped bytearray

        Returns: True if present. False if not present.
        """
        for s in self.seeds:
            h = mmh3.hash(element, s, signed=False)
            if self.bits[h % self.bits.length()] is False:
                return False
        return True

    def get_bits(self) -> bytes:
        """
        Return the filter bits.
        """
        return self.bits.tobytes()
