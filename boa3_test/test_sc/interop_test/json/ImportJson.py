from typing import Any

from boa3.builtin.interop import json
from boa3.sc.compiletime import public


@public
def main(value: Any) -> Any:
    serialized = json.json_serialize(value)
    return json.json_deserialize(serialized)
