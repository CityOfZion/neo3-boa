from typing import Any, Dict, cast

from boa3.builtin import public


@public
def Main(value: Any) -> Dict[Any, Any]:
    x = cast(dict, value)
    return x
