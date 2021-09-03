from typing import Any, List, Tuple

from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO


@public
def main() -> List[Tuple[Any, Any]]:
    return NEO.get_candidates()
