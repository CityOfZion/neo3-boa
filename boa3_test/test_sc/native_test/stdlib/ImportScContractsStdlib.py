from typing import Any

from boa3 import sc
from boa3.sc.compiletime import public


@public
def main(value: Any) -> Any:
    serialized = sc.contracts.StdLib.json_serialize(value)
    return sc.contracts.StdLib.json_deserialize(serialized)
