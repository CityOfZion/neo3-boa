from boa3.sc.compiletime import public
from boa3.sc.types import UInt160
from boa3.sc.utils import Nep11TransferEvent

transfer = Nep11TransferEvent


@public
def Main(from_addr: UInt160, to_addr: UInt160, amount: int, token_id: bytes):
    transfer(from_addr, to_addr, amount, token_id)
