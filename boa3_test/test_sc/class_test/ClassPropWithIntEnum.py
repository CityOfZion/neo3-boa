from typing import Any
from boa3.sc.types import ECPoint, NamedCurveHash
from boa3.sc.contracts import LedgerContract
from boa3.sc.compiletime import public


class Asset:
    def __init__(
            self,
            local_cid: int,
            local_nfid: int,
            asset_pubkey: ECPoint,
            elliptic_curve: int,
    ):
        self._configuration: int = local_cid
        self._public_key: ECPoint = asset_pubkey
        self._id: int = 1
        self._item: int = local_nfid
        self._active: bool = True
        self._purge_height_ils: int = 0
        self._purge_height_htls: int = LedgerContract.get_current_index()
        self._elliptic_curve = NamedCurveHash(elliptic_curve)


@public()
def main() -> Any:
    pk = ECPoint(b'\x02\x94bH\xf7\x1b\xdf\x14\x93>g5\xda\x98g\xe8\x1c\xc9\xee\xa0\xb5\x89S)\xaa\x7fq\xe7t\\\xf4\x06Y')
    return Asset(1, 2, pk, 23)
    