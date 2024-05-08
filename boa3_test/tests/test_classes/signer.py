from boa3.internal import constants
from boa3.internal.neo import from_hex_str
from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.network.payloads.signer import Signer as TestSigner
from boa3_test.test_drive.model.network.payloads.witnessscope import WitnessScope


class Signer(TestSigner):
    def __init__(self, account: UInt160, scopes: WitnessScope = WitnessScope.CalledByEntry):
        super().__init__(account, scopes)

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

    def add_permitted_groups(self, groups_pubkeys: list[bytes]):
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
