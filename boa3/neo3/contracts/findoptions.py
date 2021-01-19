from enum import IntFlag


class FindOptions(IntFlag):
    NONE = 0

    KEYS_ONLY = 1 << 0
    REMOVE_PREFIX = 1 << 1
    VALUES_ONLY = 1 << 2
    DESERIALIZE_VALUES = 1 << 3
    PICK_FIELD_0 = 1 << 4
    PICK_FIELD_1 = 1 << 5
