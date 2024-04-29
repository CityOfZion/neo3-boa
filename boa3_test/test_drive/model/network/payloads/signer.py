from typing import Any, Self

from boa3.internal.neo import from_hex_str, to_hex_str
from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope


class Signer:
    def __init__(self, account: UInt160, scopes: WitnessScope = WitnessScope.CalledByEntry):
        if scopes == WitnessScope.WitnessRules:
            raise NotImplementedError
        self._account: UInt160 = account
        self._scopes: WitnessScope = scopes
        self._allowed_contracts: list[UInt160] = []
        self._allowed_groups: list[bytes] = []

    @property
    def account(self) -> UInt160:
        return self._account

    @property
    def scopes(self) -> WitnessScope:
        return self._scopes

    def to_json(self) -> dict[str, Any]:
        return {
            'account': str(self._account),
            'scopes': self._scopes.neo_name(),
            'allowedcontracts': [str(contract_hash) for contract_hash in self._allowed_contracts],
            'allowedgroups': [to_hex_str(group_pubkey) for group_pubkey in self._allowed_groups],
            'rules': []
        }

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        account_hex = json['account']
        account = UInt160(from_hex_str(account_hex))
        scopes = WitnessScope.get_from_neo_name(json['scopes']) if 'scopes' in json else WitnessScope.CalledByEntry

        signer = cls(account, scopes)
        signer._allowed_contracts = ([UInt160(from_hex_str(contract_hex)) for contract_hex in json['allowedcontracts']]
                                     if 'allowedcontracts' in json else [])
        signer._allowed_groups = ([from_hex_str(group_hex) for group_hex in json['allowedgroups']]
                                  if 'allowedgroups' in json else [])
        return signer

    def __str__(self) -> str:
        return self._account.__str__()

    def __eq__(self, other) -> bool:
        return isinstance(other, Signer) and self._account == other._account
