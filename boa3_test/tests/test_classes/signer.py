from __future__ import annotations

from typing import Any, Dict

from boa3.neo import from_hex_str
from boa3.neo3.core.types import UInt160


class Signer:
    def __init__(self, account: UInt160):
        self._account: UInt160 = account

    @property
    def account(self) -> UInt160:
        return self._account

    def to_json(self) -> Dict[str, Any]:
        return {
            'account': str(self._account)
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Signer:
        account_hex = json['account']
        account = UInt160(from_hex_str(account_hex))
        return cls(account)

    def __str__(self) -> str:
        return self._account.__str__()
