from __future__ import annotations

from typing import Any, Dict, List

from boa3.internal import constants
from boa3.internal.neo import from_hex_str, to_hex_str
from boa3.internal.neo3.core.types import UInt160
from boa3_test.tests.test_classes.witnessscope import WitnessScope


class Signer:
    def __init__(self, account: UInt160, scopes: WitnessScope = WitnessScope.CalledByEntry):
        if scopes == WitnessScope.WitnessRules:
            raise NotImplementedError
        self._account: UInt160 = account
        self._scopes: WitnessScope = scopes
        self._allowed_contracts: List[UInt160] = []
        self._allowed_groups: List[bytes] = []
        # TODO: implement allowed witness rules

    @property
    def account(self) -> UInt160:
        return self._account

    @property
    def scopes(self) -> WitnessScope:
        return self._scopes

    def to_json(self) -> Dict[str, Any]:
        return {
            'account': str(self._account),
            'scopes': self._scopes.neo_name(),
            'allowedcontracts': [str(contract_hash) for contract_hash in self._allowed_contracts],
            'allowedgroups': [to_hex_str(group_pubkey) for group_pubkey in self._allowed_groups],
            'rules': []
        }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> Signer:
        account_hex = json['account']
        account = UInt160(from_hex_str(account_hex))
        scopes = WitnessScope.get_from_neo_name(json['scopes']) if 'scopes' in json else WitnessScope.CalledByEntry

        signer = cls(account, scopes)
        signer._allowed_contracts = ([UInt160(from_hex_str(contract_hex)) for contract_hex in json['allowedcontracts']]
                                     if 'allowedcontracts' in json else [])
        signer._allowed_groups = ([from_hex_str(group_hex) for group_hex in json['allowedgroups']]
                                  if 'allowedgroups' in json else [])
        # TODO: implement allowed witness rules
        return signer

    def __str__(self) -> str:
        return self._account.__str__()

    def __eq__(self, other) -> bool:
        return isinstance(other, Signer) and self._account == other._account

    def add_scope(self, scope: WitnessScope):
        if scope == WitnessScope.WitnessRules:
            raise NotImplementedError
        if scope > self._scopes:
            self._scopes = scope

    def add_permitted_contracts(self, contract_hashes: list):
        for contract_hash in contract_hashes:
            if isinstance(contract_hash, bytes):
                script_hash = UInt160(contract_hash)
            elif isinstance(contract_hash, str):
                script_hash = UInt160.from_string(contract_hash)
            else:
                script_hash = contract_hash

            if not isinstance(script_hash, UInt160):
                raise ValueError(f"Incorrect data type for allowed contract: {type(script_hash).__name__}")
            if script_hash not in self._allowed_contracts:
                self._allowed_contracts.append(script_hash)

    def add_permitted_groups(self, groups_pubkeys: List[bytes]):
        for group_pubkey in groups_pubkeys:
            if isinstance(group_pubkey, str):
                group = from_hex_str(group_pubkey)
            else:
                group = group_pubkey

            if not isinstance(group, bytes):
                raise ValueError(f"Incorrect data type for allowed group: {type(group).__name__}")
            elif len(group) != constants.SIZE_OF_ECPOINT:
                raise ValueError(f"Incorrect data for allowed group")
            else:
                group = bytes(group)

            if group not in self._allowed_groups:
                self._allowed_groups.append(group)

    def add_permitted_rules(self, custom_rules: list):
        raise NotImplementedError

    def set_permissions(self, permissions: list):
        if self._scopes == WitnessScope.CustomContracts:
            self.add_permitted_contracts(permissions)
        elif self._scopes == WitnessScope.CustomGroups:
            self.add_permitted_groups(permissions)
        elif self._scopes == WitnessScope.WitnessRules:
            self.add_permitted_rules(permissions)
