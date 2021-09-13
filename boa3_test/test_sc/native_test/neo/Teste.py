from boa3.builtin import public
from boa3.builtin.contract import NeoAccountState
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import UInt160


@public
def main(account: UInt160) -> NeoAccountState:
    return NEO.get_account_state(account)


@public
def transfer(from_: UInt160, to: UInt160, amount: int) -> bool:
    return NEO.transfer(from_, to, amount)
