from boa3.builtin import public
from boa3.builtin.interop.json import json_serialize


@public
def main() -> bytes:
    return json_serialize(10)
