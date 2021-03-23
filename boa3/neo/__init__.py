def to_script_hash(data_bytes: bytes) -> bytes:
    """
    Converts a data to a script hash.

    :param data_bytes: data to hash.
    :type data_bytes: bytearray or bytes

    :return: the scripthash of the data
    :rtype: bytes
    """
    from boa3.neo import cryptography
    from base58 import b58decode
    try:
        base58_decoded = b58decode(data_bytes)[1:]  # first byte is the address version

        from boa3.constants import SIZE_OF_INT160
        return bytes(base58_decoded[:SIZE_OF_INT160])
    except BaseException:
        return cryptography.hash160(data_bytes)


def to_hex_str(data_bytes: bytes) -> str:
    """
    Converts bytes into its string hex representation.

    :param data_bytes: data to represent as hex.
    :type data_bytes: bytearray or bytes

    :return: the hex representation of the data
    :rtype: str
    """
    if isinstance(data_bytes, bytes):
        data_bytes = bytearray(data_bytes)
    data_bytes.reverse()
    return '0x' + data_bytes.hex()


def from_hex_str(hex_string: str) -> bytes:
    """
    Converts a string hex representation to the equivalent bytes.

    :param hex_string: data hex representation.
    :type hex_string: str

    :return: the represented bytes
    :rtype: bytes
    """
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    data_bytes = bytearray.fromhex(hex_string)
    data_bytes.reverse()
    return bytes(data_bytes)
