from typing import Any, Dict, cast

from boa3.builtin.compile_time import public
from boa3.builtin.interop.json import json_deserialize


@public
def main() -> str:
    # compilable
    data_xy = '{"type":"skin"}'
    data: Dict[str, Any] = json_deserialize(data_xy)
    type_ = cast(str, data['type'])

    # not compilable
    if type_ == "skin":
        data_xy = '{"type":"body"}'
        data: Dict[str, Any] = json_deserialize(data_xy)
        type_ = cast(str, data['type'])  # compile error on this line

    return type_
