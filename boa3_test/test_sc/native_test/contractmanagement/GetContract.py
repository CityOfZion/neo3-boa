from typing import Optional

from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import Contract
from boa3.builtin.nativecontract.contractmanagement import ContractManagement
from boa3.builtin.type import UInt160


@public
def main(hash: UInt160) -> Optional[Contract]:
    return ContractManagement.get_contract(hash)
