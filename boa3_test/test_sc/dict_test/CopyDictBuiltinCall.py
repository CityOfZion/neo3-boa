from typing import Any, Dict, Tuple

from boa3.builtin.compile_time import public


@public
def copy_dict(dict_: Dict[Any, Any], key: Any, value: Any) -> Tuple[Dict[Any], Dict[Any]]:
    dict_copy = Dict.copy(dict_)

    dict_copy[key] = value

    dicts = (dict_, dict_copy)
    return dicts
