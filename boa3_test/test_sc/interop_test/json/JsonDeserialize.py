from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.json import json_deserialize


@public
def main(json: str) -> Any:
    return json_deserialize(json)
