from typing import Any

from boa3.builtin import interop, public


@public
def main(value: Any) -> Any:
    serialized = interop.json.json_serialize(value)
    return interop.json.json_deserialize(serialized)
