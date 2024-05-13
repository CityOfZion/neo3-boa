from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import ECPoint, UInt160


@public
def main(account: UInt160, pubkey: ECPoint) -> bool:
    return NeoToken.vote(account, pubkey)


@public
def un_vote(account: UInt160) -> bool:
    return NeoToken.un_vote(account)
