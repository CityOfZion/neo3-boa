from boa3.builtin.compile_time import public
from boa3.builtin.interop.json import json_serialize


@public
def main() -> str:
    return json_serialize(True)
