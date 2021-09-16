from __future__ import annotations

from typing import Any, Dict

from boa3.neo import from_hex_str
from boa3.neo3.core.types import UInt160
from boa3_test.tests.test_classes.witnessscope import WitnessScope


class Signer:
    def __init__(self, account: UInt160, scopes: WitnessScope = WitnessScope.CalledByEntry):
        self._account: UInt160 = account
        self._scopes: WitnessScope = scopes

    @property
    def account(self) -> UInt160:
        return self._account

    @property
    def scopes(self) -> WitnessScope:
        return self._scopes

    def to_json(self) -> Dict[str, Any]:
        return {
            'account': str(self._account),
            'scopes': self._scopes.neo_name()
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Signer:
        account_hex = json['account']
        account = UInt160(from_hex_str(account_hex))
        scopes = WitnessScope.get_from_neo_name(json['scopes']) if 'scopes' in json else WitnessScope.CalledByEntry
        return cls(account, scopes)

    def __str__(self) -> str:
        return self._account.__str__()

    def __eq__(self, other) -> bool:
        return isinstance(other, Signer) and self._account == other._account
