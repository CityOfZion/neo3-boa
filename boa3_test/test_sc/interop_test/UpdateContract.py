from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.contract import update_contract


@public
def Main(script: bytes, manifest: bytes):
    update_contract(script, manifest)
