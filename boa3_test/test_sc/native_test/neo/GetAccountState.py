from boa3.builtin.compile_time import public
from boa3.builtin.contract import NeoAccountState
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import UInt160


@public
def main(account: UInt160) -> NeoAccountState:
    return NEO.get_account_state(account)
