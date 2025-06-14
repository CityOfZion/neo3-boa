from typing import Any

from boa3.sc.types import CallFlags
from boa3.sc.utils import call_contract


def Main(scripthash: bytes, method: str, arg0: Any, arg1: Any, flags: CallFlags):
    call_contract(scripthash, method, arg0, arg1, flags)
