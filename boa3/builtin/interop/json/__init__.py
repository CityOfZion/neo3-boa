from typing import Any


def json_serialize(item: Any) -> bytes:
    """
    Serializes an item into a json

    :param item: The item that will serialized
    :type item: Any
    :return: The serialized item
    :rtype: bytes

    :raise Exception: raised if item is an int value greater than MAX_SAFE_INTEGER or lower than MIN_SAFE_INTEGER, if
        item is a dictionary that have a bytearray as key, if item isn't serializable or if item is too big.
    """
    pass


def json_deserialize(json: bytes) -> Any:
    """
    Deserializes a json into some valid type

    :param json: A json that will be deserialized
    :type json: bytes
    :return: The deserialized json
    :rtype: Any

    :raise Exception: raised if json's deserialization is not valid
    """
    pass
