from typing import Any, cast

from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main() -> str:
    # compilable
    data_xy = '{"type":"skin"}'
    data: dict[str, Any] = StdLib.json_deserialize(data_xy)
    type_ = cast(str, data['type'])

    # not compilable
    if type_ == "skin":
        data_xy = '{"type":"body"}'
        data: dict[str, Any] = StdLib.json_deserialize(data_xy)
        type_ = cast(str, data['type'])  # compile error on this line

    return type_
