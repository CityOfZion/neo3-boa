__all__ = [
    'json_serialize',
    'json_deserialize',
]


from typing import Any


def json_serialize(item: Any) -> str:
    """
    Serializes an item into a json.

    >>> json_serialize({'one': 1, 'two': 2, 'three': 3})
    '{"one":1,"two":2,"three":3}'

    :param item: The item that will be serialized
    :type item: Any
    :return: The serialized item
    :rtype: str

    :raise Exception: raised if the item is an integer value out of the Neo's accepted range, is a dictionary with a
        bytearray key, or isn't serializable.
    """
    pass


def json_deserialize(json: str) -> Any:
    """
    Deserializes a json into some valid type.

    >>> json_deserialize('{"one":1,"two":2,"three":3}')
    {'one': 1, 'three': 3, 'two': 2}

    :param json: A json that will be deserialized
    :type json: str
    :return: The deserialized json
    :rtype: Any

    :raise Exception: raised if jsons deserialization is not valid.
    """
    pass
