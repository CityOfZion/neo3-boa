from typing import Any

from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(json: bytes) -> Any:
    return StdLib.json_deserialize(json)
