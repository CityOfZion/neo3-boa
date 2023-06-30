from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop.blockchain import get_contract
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160


@public
def main(hash: UInt160) -> Optional[Contract]:
    return get_contract(hash)
