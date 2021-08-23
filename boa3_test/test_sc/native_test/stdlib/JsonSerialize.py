from typing import Any

from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(item: Any) -> bytes:
    return StdLib.json_serialize(item)
