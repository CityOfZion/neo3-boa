from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.contract.contract import Contract


@public
def Main(value: Any) -> bool:
    # not supported because boa builtin classes don't work with isinstance yet
    return isinstance(value, Contract)
