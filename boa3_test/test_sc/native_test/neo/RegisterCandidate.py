from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import ECPoint


@public
def main(pubkey: ECPoint) -> bool:
    return NeoToken.register_candidate(pubkey)
