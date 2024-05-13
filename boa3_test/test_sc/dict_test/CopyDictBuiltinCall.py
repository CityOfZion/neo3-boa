from typing import Any

from boa3.sc.compiletime import public


@public
def copy_dict(dict_: dict[Any, Any], key: Any, value: Any) -> tuple[dict[Any, Any], dict[Any, Any]]:
    dict_copy = dict.copy(dict_)

    dict_copy[key] = value

    dicts = (dict_, dict_copy)
    return dicts
