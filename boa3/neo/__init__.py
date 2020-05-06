def to_script_hash(data_bytes: bytes) -> bytes:
    """
    Converts a data to a script hash.

    :param data_bytes: data to hash.
    :type data_bytes: bytearray or bytes

    :return: the scripthash of the data
    :rtype: bytes
    """
    from boa3.neo import cryptography
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
    return data_bytes.hex()
