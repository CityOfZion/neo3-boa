from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def main(option: FindOptions) -> FindOptions:
    return option


@public
def option_keys_only() -> FindOptions:
    return FindOptions.KEYS_ONLY


@public
def option_remove_prefix() -> FindOptions:
    return FindOptions.REMOVE_PREFIX


@public
def option_values_only() -> FindOptions:
    return FindOptions.VALUES_ONLY


@public
def option_deserialize_values() -> FindOptions:
    return FindOptions.DESERIALIZE_VALUES


@public
def option_pick_field_0() -> FindOptions:
    return FindOptions.PICK_FIELD_0


@public
def option_pick_field_1() -> FindOptions:
    return FindOptions.PICK_FIELD_1


@public
def option_backwards() -> FindOptions:
    return FindOptions.BACKWARDS
