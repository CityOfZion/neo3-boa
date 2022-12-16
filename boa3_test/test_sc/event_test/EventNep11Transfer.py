from boa3.builtin.compile_time import public
from boa3.builtin.contract import Nep11TransferEvent
from boa3.builtin.type import UInt160

transfer = Nep11TransferEvent


@public
def Main(from_addr: UInt160, to_addr: UInt160, amount: int, token_id: bytes):
    transfer(from_addr, to_addr, amount, token_id)
