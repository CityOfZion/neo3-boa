from typing import Any

from boa3.builtin.compile_time import public


@public
def main(dict_: dict[Any, Any], key: Any) -> tuple[dict[Any, Any], Any]:
    value = dict_.pop(key)
    new_dict_and_value = (dict_, value)
    return new_dict_and_value
