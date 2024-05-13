from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.runtime import script_container


@public
def main() -> Any:
    return script_container
