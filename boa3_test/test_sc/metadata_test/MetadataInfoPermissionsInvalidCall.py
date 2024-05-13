from typing import Any

from boa3.sc.compiletime import NeoMetadata, public
from boa3.sc.contracts import NeoToken
from boa3.sc.utils import call_contract


def permissions_manifest() -> NeoMetadata:
    meta = NeoMetadata()

    meta.add_permission(contract='0x0102030405060708090A0B0C0D0E0F1011121314', methods='*')

    return meta


@public
def main() -> Any:
    return call_contract(NeoToken.hash, 'transfer', [NeoToken.hash, NeoToken.hash, 1, None])
