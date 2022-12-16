from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(json: str) -> Any:
    return StdLib.json_deserialize(json)
