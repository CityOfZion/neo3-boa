from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.contracts import NeoToken


@public
def main() -> int:
    return NeoToken.totalSupply()


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='*', methods='*')

    return meta
