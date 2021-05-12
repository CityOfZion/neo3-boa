from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.runtime import get_script_container


@public
def main() -> Any:
    return get_script_container
