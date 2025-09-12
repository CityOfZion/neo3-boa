from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import stdlib


@public
def main(value: Any) -> Any:
    serialized = stdlib.StdLib.json_serialize(value)
    return stdlib.StdLib.json_deserialize(serialized)
