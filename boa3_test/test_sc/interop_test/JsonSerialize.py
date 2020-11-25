from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.json import json_serialize


@public
def main(item: Any) -> bytes:
    return json_serialize(item)
