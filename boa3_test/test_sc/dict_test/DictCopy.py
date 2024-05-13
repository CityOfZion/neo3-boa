from typing import Any

from boa3.sc.compiletime import public


@public
def copy_dict(dict_: dict[Any, Any]) -> list[dict[Any, Any]]:
    dict_copy = dict_.copy()
    dict_copy['unit'] = 'test'
    return [dict_, dict_copy]
