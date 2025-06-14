from typing import Any

from boa3.sc import runtime, storage
from boa3.sc.compiletime import public


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
        container = runtime.script_container
        storage.put_uint160(b'owner', container.sender)
    else:
        return
