from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(json: str) -> Any:
    return StdLib.json_deserialize(json)
