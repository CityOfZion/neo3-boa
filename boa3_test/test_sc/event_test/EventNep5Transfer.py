from boa3.builtin import public

from boa3.builtin.contract import Nep5TransferEvent


transfer = Nep5TransferEvent


@public
def Main(from_addr: bytes, to_addr: bytes, amount: int):
    transfer(from_addr, to_addr, amount)
