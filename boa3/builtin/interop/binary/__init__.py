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
