from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.types import UInt160


@public
def main() -> UInt160:
    return NeoToken.get_committee_address()
