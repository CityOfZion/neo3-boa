from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.json import json_serialize


@public
def main(item: Any) -> str:
    return json_serialize(item)
