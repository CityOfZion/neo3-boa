from typing import Any


def json_serialize(item: Any) -> bytes:
    """
    Serializes an item into a json

    :param item: The item that will be serialized
    :type item: Any
    :return: The serialized item
    :rtype: bytes

    :raise Exception: raised if the item is an integer value out of the Neo's accepted range, is a dictionary with a
        bytearray key, or isn't serializable.
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
