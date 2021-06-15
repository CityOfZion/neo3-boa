from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.runtime import script_container


@public
def main() -> Any:
    return script_container
