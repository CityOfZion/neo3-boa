from typing import Any


def base58_encode(key: bytes) -> str:
    """
    Encodes a bytes value using base58

    :param key: string value to be encoded
    :type key: bytes
    :return: the encoded string as bytes.
    :rtype: str
    """
    pass


def base58_decode(key: str) -> bytes:
    """
    Decodes a string value encoded with base58

    :param key: bytes value to be decoded
    :type key: str
    :return: the decoded bytes as string.
    :rtype: bytes
    """
    pass


def base64_encode(key: bytes) -> str:
    """
    Encodes a bytes value using base64

    :param key: bytes value to be encoded
    :type key: bytes
    :return: the encoded bytes as string.
    :rtype: str
    """
    pass


def base64_decode(key: str) -> bytes:
    """
    Decodes a string value encoded with base64

    :param key: string value to be decoded
    :type key: string
    :return: the decoded string as bytes.
    :rtype: bytes
    """
    pass


def serialize(item: Any) -> bytes:
    """
    Serializes the given value into its bytes representation

    :param item: value to be serialized
    :type item: Any
    :return: the serialized value
    :rtype: bytes

    :raise Exception: raised if the item's type is not serializable.
    """
    pass


def deserialize(data: bytes) -> Any:
    """
    Deserializes the given bytes value

    :param data: serialized value
    :type data: bytes
    :return: the deserialized result
    :rtype: Any

    :raise Exception: raised when the date doesn't represent a serialized value.
    """
    pass


def atoi(value: str, base: int = 10) -> int:
    """
    Converts a character string to a specific base value, decimal or hexadecimal. The default is decimal.

    :param value: the int value as a string
    :type value: str
    :param base: the value base
    :type base: int
    :return: the equivalent value
    :rtype: int

    :raise Exception: raised when base isn't 10 or 16.
    """
    pass


def itoa(value: int, base: int = 10) -> str:
    """
    Converts the specific type of value to a decimal or hexadecimal string. The default is decimal.

    :param value: the int value
    :type value: int
    :param base: the value's base
    :type base: int

    :return: The converted string
    :rtype: int
    """
    pass
