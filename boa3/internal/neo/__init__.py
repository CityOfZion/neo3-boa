from typing import Union


def to_script_hash(data_bytes: bytes) -> bytes:
    """
    Converts a data to a script hash.

    :param data_bytes: data to hash.
    :type data_bytes: bytearray or bytes

    :return: the scripthash of the data
    :rtype: bytes
    """
    from boa3.internal.neo import cryptography
    from base58 import b58decode
    try:
        base58_decoded = b58decode(data_bytes)[1:]  # first byte is the address version

        from boa3.internal.constants import SIZE_OF_INT160
        if len(base58_decoded) < SIZE_OF_INT160:
            raise ValueError
        return bytes(base58_decoded[:SIZE_OF_INT160])
    except BaseException:
        return cryptography.hash160(data_bytes)


def public_key_to_script_hash(public_key: Union[str, bytes]) -> bytes:
    """
    Converts a public key bytes sequence to a script hash.

    :return: the script hash of the data
    :rtype: bytes
    """
    if isinstance(public_key, str):
        public_key = from_hex_str(public_key)

    from boa3.internal.constants import SIZE_OF_ECPOINT

    if len(public_key) != SIZE_OF_ECPOINT:
        # it's not a public key
        return to_script_hash(public_key)

    # public keys must include a check sig script when converting to script hash
    from boa3.internal.neo.vm.opcode.Opcode import Opcode
    from boa3.internal.neo.vm.type.Integer import Integer
    from boa3.internal.model.builtin.interop.crypto.checksigmethod import CheckSigMethod

    check_sig_arg = Opcode.PUSHDATA1 + Integer(SIZE_OF_ECPOINT).to_byte_array() + public_key
    check_sig_call = CheckSigMethod.get_raw_bytes()
    return to_script_hash(check_sig_arg + check_sig_call)


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
    data_copy = data_bytes.copy()
    data_copy.reverse()
    return '0x' + data_copy.hex()


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
