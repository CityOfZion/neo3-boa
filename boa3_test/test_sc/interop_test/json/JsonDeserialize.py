from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.json import json_deserialize


@public
def main(json: str) -> Any:
    return json_deserialize(json)
