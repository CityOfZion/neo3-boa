from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import ECPoint, UInt160


@public
def main(account: UInt160, pubkey: ECPoint) -> bool:
    return NEO.vote(account, pubkey)
