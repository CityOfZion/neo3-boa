from boa3.sc.compiletime import public
from boa3.sc.types import UInt160
from boa3.sc.utils import Nep17TransferEvent

transfer = Nep17TransferEvent


@public
def Main(from_addr: UInt160, to_addr: UInt160, amount: int):
    transfer(from_addr, to_addr, amount)
