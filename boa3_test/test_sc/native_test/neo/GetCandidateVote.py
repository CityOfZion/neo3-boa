from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import ECPoint


@public
def main(pubkey: ECPoint) -> int:
    return NEO.get_candidate_vote(pubkey)
