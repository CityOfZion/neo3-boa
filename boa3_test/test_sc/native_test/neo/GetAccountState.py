from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160, NeoAccountState


@public
def main(account: UInt160) -> NeoAccountState:
    return NeoToken.get_account_state(account)
