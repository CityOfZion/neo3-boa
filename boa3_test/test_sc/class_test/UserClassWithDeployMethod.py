from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime, storage
from boa3.builtin.interop.blockchain import Transaction


class Example:
    def __init__(self):
        self.val1 = 1
        self.val2 = 2


@public
def get_obj() -> Example:
    return Example()


@public
def _deploy(data: Any, update: bool):
    if not update:
        # setup instructions that will be executed when the smart contract is deployed
        container: Transaction = runtime.script_container
        storage.put(b'owner', container.sender)
    else:
        return
