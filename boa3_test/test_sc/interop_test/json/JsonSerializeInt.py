from boa3.builtin import public
from boa3.builtin.interop.json import json_serialize


@public
def main() -> str:
    return json_serialize(10)
