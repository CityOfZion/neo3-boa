from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(item: Any) -> str:
    return StdLib.json_serialize(item)
