from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import ECPoint


@public
def main() -> list[ECPoint]:
    return NeoToken.get_next_block_validators()
