from typing import Any, Dict, List

from boa3.builtin.compile_time import public


@public
def copy_dict(dict_: Dict[Any, Any]) -> List[Dict[Any, Any]]:
    dict_copy = dict_.copy()
    dict_copy['unit'] = 'test'
    return [dict_, dict_copy]
