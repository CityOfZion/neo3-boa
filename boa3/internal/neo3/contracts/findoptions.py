from enum import IntEnum


class FindOptions(IntEnum):
    """
    Represents the options you can use when trying to find a set of values inside the storage.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/services/FindOptions>`__
    to learn more about the FindOption class.
    """
    NONE = 0
    """
    No option is set. The results will be an iterator of (key, value).

    :meta hide-value:
    """

    KEYS_ONLY = 1 << 0
    """
    Indicates that only keys need to be returned. The results will be an iterator of keys.

    :meta hide-value:
    """

    REMOVE_PREFIX = 1 << 1
    """
    Indicates that the prefix byte of keys should be removed before return.

    :meta hide-value:
    """

    VALUES_ONLY = 1 << 2
    """
    Indicates that only values need to be returned. The results will be an iterator of values.

    :meta hide-value:
    """

    DESERIALIZE_VALUES = 1 << 3
    """
    Indicates that values should be deserialized before return.

    :meta hide-value:
    """

    PICK_FIELD_0 = 1 << 4
    """
    Indicates that only the field 0 of the deserialized values need to be returned.
    This flag must be set together with DESERIALIZE_VALUES, e.g., `DESERIALIZE_VALUES | PICK_FIELD_0`

    :meta hide-value:
    """

    PICK_FIELD_1 = 1 << 5
    """
    Indicates that only the field 1 of the deserialized values need to be returned.
    This flag must be set together with DESERIALIZE_VALUES, e.g., `DESERIALIZE_VALUES | PICK_FIELD_1`

    :meta hide-value:
    """

    BACKWARDS = 1 << 7
    """
    Indicates that results should be returned in backwards (descending) order.

    :meta hide-value:
    """
