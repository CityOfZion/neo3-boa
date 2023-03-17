import hashlib


def hash160(byte_array: bytes) -> bytes:
    """
    Get a hash of the provided message using the ripemd160 algorithm.

    :param byte_array: data to hash.
    :type byte_array: bytes

    :return: hashed data
    :rtype: bytes
    """
    intermed = sha256(byte_array)
    return hashlib.new('ripemd160', intermed).digest()


def sha256(byte_array: bytes) -> bytes:
    """
    Perform a SHA256 operation on the input.

    :param byte_array: data to hash.
    :type byte_array: bytes

    :return: hashed data
    :rtype: bytes
    """
    return hashlib.sha256(byte_array).digest()
