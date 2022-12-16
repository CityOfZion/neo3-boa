from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import ECPoint, UInt160


@public
def main(account: UInt160, pubkey: ECPoint) -> bool:
    return NEO.vote(account, pubkey)


@public
def un_vote(account: UInt160) -> bool:
    return NEO.un_vote(account)
