from typing import Any, Dict, Tuple

from boa3.builtin.compile_time import public


@public
def main(dict_: Dict[Any, Any], key: Any) -> Tuple[Dict[Any, Any], Any]:
    value = dict_.pop(key)
    new_dict_and_value = (dict_, value)
    return new_dict_and_value
