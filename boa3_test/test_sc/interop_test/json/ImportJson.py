from typing import Any

from boa3.builtin import public
from boa3.builtin.interop import json


@public
def main(value: Any) -> Any:
    serialized = json.json_serialize(value)
    return json.json_deserialize(serialized)
